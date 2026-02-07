#!/usr/bin/env python3
"""
Boot Menu mejorado con:
- Scroll automático para más de 3 opciones
- Opción Exit para cerrar limpiamente
- Mejor visualización
"""

import time
import subprocess
import sys  # ⭐ Añadido para sys.exit()
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
import os

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pines de botones
PIN_DOWN = 22
PIN_UP = 9
PIN_OK = 25

# Configura botones con pull-up
GPIO.setup(PIN_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_OK, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# OLED
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

# Fuente
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
except:
    font = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Items del menú
menu_items = [
    "Looper",
    "Practice Player",
    "Bluetooth Rec",
    "Shutdown",
    "Exit"
]

selected = 0
scroll_offset = 0  # Para scroll
MAX_VISIBLE = 3    # Máximo de items visibles a la vez

def draw_menu():
    """Dibuja el menú con scroll si hay más de 3 opciones"""
    global scroll_offset
    
    img = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(img)
    
    # Título
    draw.text((5, 2), "BOOT MENU", font=font_small, fill=255)
    draw.line([(0, 15), (128, 15)], fill=255)
    
    # Ajustar scroll para mantener el item seleccionado visible
    if selected < scroll_offset:
        scroll_offset = selected
    elif selected >= scroll_offset + MAX_VISIBLE:
        scroll_offset = selected - MAX_VISIBLE + 1
    
    # Dibujar items visibles
    for i in range(MAX_VISIBLE):
        item_index = scroll_offset + i
        
        if item_index >= len(menu_items):
            break
        
        item = menu_items[item_index]
        y_pos = 20 + i * 15
        
        # Marcar seleccionado
        if item_index == selected:
            # Rectángulo de selección
            draw.rectangle([(2, y_pos - 2), (126, y_pos + 13)], outline=255, fill=0)
            draw.text((10, y_pos), f"> {item}", font=font_small, fill=255)
        else:
            draw.text((10, y_pos), f"  {item}", font=font_small, fill=255)
    
    # Indicadores de scroll
    if scroll_offset > 0:
        # Flecha arriba
        draw.polygon([(120, 18), (124, 22), (116, 22)], fill=255)
    
    if scroll_offset + MAX_VISIBLE < len(menu_items):
        # Flecha abajo
        draw.polygon([(120, 62), (124, 58), (116, 58)], fill=255)
    
    # Mostrar contador
    draw.text((2, 58), f"{selected + 1}/{len(menu_items)}", font=font_small, fill=255)
    
    device.display(img)

def navigate_down():
    """Navega hacia abajo (circular)"""
    global selected
    selected = (selected + 1) % len(menu_items)
    draw_menu()

def navigate_up():
    """Navega hacia arriba (circular)"""
    global selected
    selected = (selected - 1) % len(menu_items)
    draw_menu()
    
def cleanup_and_exit():
    """Limpia recursos y sale limpiamente"""
    print("\nLimpiando recursos...")
    
    # Limpiar pantalla
    img = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(img)
    draw.text((30, 25), "Goodbye!", font=font, fill=255)
    device.display(img)
    time.sleep(1)
    
    # Limpiar OLED completamente
    img = Image.new("1", (128, 64))
    device.display(img)
    
    # ⭐ NO hacer GPIO.cleanup() - corrompe I2C y AudioInjector
    # Solo limpiar los pines específicos que usamos
    try:
        GPIO.setup(PIN_DOWN, GPIO.IN)  # Resetear a input
        GPIO.setup(PIN_UP, GPIO.IN)
        GPIO.setup(PIN_OK, GPIO.IN)    # Resetear a input
    except:
        pass
    
    print("Boot menu cerrado limpiamente")
    # ⭐ Usar exit() normal en vez de os._exit(0)
    sys.exit(0)

def select():
    """Ejecuta la acción del item seleccionado"""
    selection = menu_items[selected]
    
    if selection == "Looper":
        print("Arrancando Looper...")
        
        # Mensaje en pantalla
        img = Image.new("1", (128, 64))
        draw = ImageDraw.Draw(img)
        draw.text((20, 25), "Starting", font=font, fill=255)
        draw.text((25, 40), "Looper...", font=font_small, fill=255)
        device.display(img)
        time.sleep(0.5)
        
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
            stdout=open('/tmp/looper.log', 'w', buffering=1),
            stderr=open('/tmp/looper_errors.log', 'w', buffering=1),
            start_new_session=True
        )
        
        # Termina boot_menu
        os._exit(0)
        
    elif selection == "Practice Player":
        print("Arrancando Practice Player...")
        
        # Mensaje en pantalla
        img = Image.new("1", (128, 64))
        draw = ImageDraw.Draw(img)
        draw.text((15, 25), "Starting", font=font, fill=255)
        draw.text((10, 40), "Practice...", font=font_small, fill=255)
        device.display(img)
        time.sleep(0.5)
        
        # Limpia pantalla
        img = Image.new("1", (128, 64))
        device.display(img)
        
        # Limpia GPIO
        GPIO.cleanup()
        
        # Lanza practice player
        subprocess.Popen(
            ["/home/Javo/Proyects/practice_player/practice_env/bin/python", "-u", "main.py"],
            cwd="/home/Javo/Proyects/practice_player",
            stdin=subprocess.DEVNULL,
            stdout=open('/tmp/practice_player.log', 'w', buffering=1),
            stderr=open('/tmp/practice_player_errors.log', 'w', buffering=1),
            start_new_session=True
        )
        
        # Termina boot_menu
        os._exit(0)

    
    elif selection == "Bluetooth Rec":
        print("Arrancando Bluetooth Recorder...")
        
        # Mensaje en pantalla
        img = Image.new("1", (128, 64))
        draw = ImageDraw.Draw(img)
        draw.text((15, 25), "Starting", font=font, fill=255)
        draw.text((10, 40), "BT Rec...", font=font_small, fill=255)
        device.display(img)
        time.sleep(0.5)
        
        # Limpia pantalla
        img = Image.new("1", (128, 64))
        device.display(img)
        
        # Limpia GPIO
        GPIO.cleanup()
        
        # Lanza practice player
        subprocess.Popen(
            ["/home/Javo/Proyects/bluetooth_recorder/bt_recorder_env/bin/python", "-u", "main.py"],
            cwd="/home/Javo/Proyects/bluetooth_recorder",
            stdin=subprocess.DEVNULL,
            stdout=open('/tmp/bluetooth_recorder.log', 'w', buffering=1),
            stderr=open('/tmp/bluetooth_recorder_errors.log', 'w', buffering=1),
            start_new_session=True
        )
        
        # Termina boot_menu
        os._exit(0)
    
    elif selection == "Shutdown":
        print("Apagando sistema...")
        
        # Mensaje en pantalla
        img = Image.new("1", (128, 64))
        draw = ImageDraw.Draw(img)
        draw.text((15, 25), "Shutting", font=font, fill=255)
        draw.text((25, 40), "down...", font=font_small, fill=255)
        device.display(img)
        time.sleep(1)
        
        # Limpia pantalla
        img = Image.new("1", (128, 64))
        device.display(img)
        
        GPIO.cleanup()
        subprocess.run(["sudo", "shutdown", "-h", "now"])
    
    elif selection == "Exit":
        cleanup_and_exit()

# Dibuja menú inicial
print("=== Boot Menu Iniciado ===")
draw_menu()
print(f"Items disponibles: {', '.join(menu_items)}")
print("Usa botones: ↓ (GPIO23) y OK (GPIO22)")

# Loop principal

try:
    last_down = True
    last_up = True  # ⭐ Ya está declarado
    last_ok = True
    
    while True:
        # Lee botones (LOW = presionado porque usamos pull-up)
        current_down = GPIO.input(PIN_DOWN)
        current_up = GPIO.input(PIN_UP)  # ⭐ Ya está declarado
        current_ok = GPIO.input(PIN_OK)
        
        # Detecta flanco descendente (presión)
        if last_down and not current_down:  # Botón DOWN presionado
            time.sleep(0.05)  # Debounce
            if not GPIO.input(PIN_DOWN):  # Confirma que sigue presionado
                navigate_down()
        
        # ⭐ AÑADE ESTO AQUÍ:
        if last_up and not current_up:  # Botón UP presionado
            time.sleep(0.05)  # Debounce
            if not GPIO.input(PIN_UP):  # Confirma que sigue presionado
                navigate_up()
        
        if last_ok and not current_ok:  # Botón OK presionado
            time.sleep(0.05)  # Debounce
            if not GPIO.input(PIN_OK):  # Confirma que sigue presionado
                select()
        
        last_down = current_down
        last_up = current_up  # ⭐ AÑADE ESTO TAMBIÉN
        last_ok = current_ok        
        time.sleep(0.01)  # Pequeña pausa para no saturar CPU
        
except KeyboardInterrupt:
    print("\nCtrl+C detectado")
    cleanup_and_exit()
    
except Exception as e:
    print(f"\nError en boot_menu: {e}")
    cleanup_and_exit()
    
finally:
    # ⭐ NO hacer GPIO.cleanup() - puede corromper I2C
    # El sistema operativo limpiará los pines al terminar el proceso
    pass
