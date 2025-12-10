#!/usr/bin/env python3
import time
import subprocess
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button, Device
import os
#import RPi.GPIO as GPIO


#from gpiozero.pins.rpigpio import RPiGPIOFactory
from gpiozero.pins.pigpio import PiGPIOFactory

# Limpia GPIO al inicio
Device.pin_factory = PiGPIOFactory()

#solo usa RPi.GPIO para limpiar, de resto va de gpiozero
#GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()

#CONFIGURA TU OLED AQUI
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)  # cambia segun tu modelo
#

# Botones del menu (elige 3 GPIOs libres, ej: 16, 20, 21)
#btn_up    = Button(17, pull_up=True, bounce_time=0.03)
btn_down  = Button(23, pull_up=True, bounce_time=0.03)
btn_ok    = Button(22, pull_up=True, bounce_time=0.03, hold_time=1)

menu_items = ["Looper", "Shutdown"]
selected = 0

def draw_menu():
    img = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(img)
    
    for i, item in enumerate(menu_items):
        prefix = "> " if i == selected else "  "
        draw.text((10, 20 + i*20), prefix + item, fill=255)
    
    device.display(img)
    
#def navigate_up():
#    global selected
#    selected = (selected - 1) % len(menu_items)
#    draw_menu()

def navigate_down():
    global selected
    selected = (selected + 1) % len(menu_items)
    draw_menu()

def select():
    if menu_items[selected] == "Looper":
        print("Arrancando Looper...")
        env = os.environ.copy()
        env["PYTHONPATH"] = "/home/Javo/Proyects/Looper"
        subprocess.Popen(
        	["/home/Javo/Proyects/Looper/looper_env/bin/python", "-m", "software.main"], cwd="/home/Javo/Proyects/Looper"
        	)
        time.sleep(2)  # da tiempo a que arranque y limpie la pantalla si quieres
    elif menu_items[selected] == "Shutdown":
        print("Apagando sistema...")
        subprocess.run(["sudo", "shutdown", "-h", "now"])

# Eventos
#btn_up.when_pressed = navigate_up
btn_down.when_pressed = navigate_down
btn_ok.when_pressed = select

# Primera dibujada
draw_menu()
print("Menú de arranque activo. Usa ↑ ↓ OK")

# Espera eterna
while True:
    time.sleep(1)
