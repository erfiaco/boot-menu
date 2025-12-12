#!/usr/bin/env python3
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image

# Configura OLED
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

# Limpia pantalla
img = Image.new("1", (128, 64))
device.display(img)

print("Pantalla limpiada")
