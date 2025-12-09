#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Todos los GPIO que tienen pin fisico en cualquier modelo de Raspberry Pi
BOTONES = [
    2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
    12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
    22, 23, 24, 25, 26, 27
]

DEBOUNCE = 0.05  # tiempo antirebote en segundos

GPIO.setmode(GPIO.BCM)

# Configurar todos como entrada con pull-up interno
for pin in BOTONES:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Detectando pulsaciones en todos los GPIO...")
print("Conecta cada boton entre el GPIO y GND")
print("Pulsa Ctrl+C para salir\n")

try:
    ultimo_estado = {pin: GPIO.HIGH for pin in BOTONES}
    ultima_pulsacion = {pin: 0 for pin in BOTONES}

    while True:
        for pin in BOTONES:
            estado = GPIO.input(pin)

            # Flanco descendente = boton pulsado
            if ultimo_estado[pin] == GPIO.HIGH and estado == GPIO.LOW:
                ahora = time.time()
                if ahora - ultima_pulsacion[pin] > DEBOUNCE:
                    print(f"Boton pulsado en GPIO {pin} (BCM)")
                    ultima_pulsacion[pin] = ahora

            ultimo_estado[pin] = estado

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nPrograma terminado")
finally:
    GPIO.cleanup()
