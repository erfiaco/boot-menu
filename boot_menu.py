#!/usr/bin/env python3
import time
import subprocess
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw
import RPi.GPIO as GPIO
import os

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pines de botones
PIN_DOWN = 23
PIN_OK = 22

# Configura botones con pull-up
GPIO.setup(PIN_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_OK, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# OLED
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

menu_items = ["Looper", "Shutdown"]
selected = 0

def draw_menu():
    img = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(img)
    
    for i, item in enumerate(menu_items):
        prefix = "> " if i == selected else "  "
        draw.text((10, 20 + i*20), prefix + item, fill=255)
    
    device.display(img)

def navigate_down():
    global selected
    selected = (selected + 1) % len(menu_items)
    draw_menu()

def select():
    if menu_items[selected] == "Looper":
        print("Arrancando Looper...")
        # Limpia pantalla
        img = Image.new("1", (128, 64))
        device.display(img)
        
        # Limpia GPIO
        GPIO.cleanup()
        
        # Lanza looper
        subprocess.Popen(
            ["/home/Javo/Proyects/Looper/looper_env/bin/python", "-u", "-m", "software.main"],
            cwd="/home/Javo/Proyects/Looper",
            stdin=subprocess.DEVNULL,
#            stdout=subprocess.DEVNULL,
#            stderr=subprocess.DEVNULL,
            stdout=open('/tmp/looper.log', 'w', buffering=1),   # ← Añade
            stderr=open('/tmp/looper_errors.log', 'w', buffering=1),  # ← Añade
            start_new_session=True      # ← Añade esto (CLAVE)
            

        )
        
        # Termina boot_menu
        import os
        os._exit(0)

    elif menu_items[selected] == "Practice_player":
        print("Practice player...")
        # Limpia pantalla
        img = Image.new("1", (128, 64))
        device.display(img)
        
        # Limpia GPIO
        GPIO.cleanup()        

        # Lanza practice player
        subprocess.Popen(
            ["/home/Javo/Proyects/practice_player/reproductor_env/bin/python", "-u", "-m", "main"],
            cwd="/home/Javo/Proyects/practice_player",
            stdin=subprocess.DEVNULL,
#            stdout=subprocess.DEVNULL,
#            stderr=subprocess.DEVNULL,
            stdout=open('/tmp/practice_player.log', 'w', buffering=1),   # ← Añade
            stderr=open('/tmp/practice_player_errors.log', 'w', buffering=1),  # ← Añade
            start_new_session=True      # ← Añade esto (CLAVE)
        
    elif menu_items[selected] == "Shutdown":
        print("Apagando sistema...")
        
        # Limpia pantalla ANTES de apagar
        img = Image.new("1", (128, 64))
        device.display(img)
        
        GPIO.cleanup()
        subprocess.run(["sudo", "shutdown", "-h", "now"])
    
    

# Dibuja menú inicial
draw_menu()
print("Menú de arranque activo. Usa ↓ OK")

# Loop principal
try:
    last_down = True
    last_ok = True
    
    while True:
        # Lee botones (LOW = presionado porque usamos pull-up)
        current_down = GPIO.input(PIN_DOWN)
        current_ok = GPIO.input(PIN_OK)
        
        # Detecta flanco descendente (presión)
        if last_down and not current_down:
            time.sleep(0.05)  # Debounce
            navigate_down()
        
        if last_ok and not current_ok:
            time.sleep(0.05)  # Debounce
            select()
        
        last_down = current_down
        last_ok = current_ok
        
        time.sleep(0.01)  # Pequeña pausa
        
except KeyboardInterrupt:
    print("\nSaliendo...")
finally:
    GPIO.cleanup()
