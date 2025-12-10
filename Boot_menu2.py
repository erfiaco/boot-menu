#!/usr/bin/env python3
"""
Boot Menu SIMPLE - Sin complicaciones con I2C
"""
import sys
import time
import signal

# Flag para controlar la salida
running = True

def salir_limpiamente(signum, frame):
    """Salir cuando el usuario presione Ctrl+C"""
    global running
    print("\n\n👋 Saliendo del Boot Menu...")
    running = False
    sys.exit(0)

# Configurar Ctrl+C
signal.signal(signal.SIGINT, salir_limpiamente)

print("=" * 40)
print("       BOOT MENU - Raspberry Pi")
print("=" * 40)

try:
    # INTENTAR cargar el OLED (opcional)
    try:
        from luma.core.interface.serial import i2c
        from luma.oled.device import ssd1306
        
        print("🔄 Inicializando pantalla OLED...")
        serial = i2c(port=1, address=0x3C)
        oled = ssd1306(serial, width=128, height=64)
        
        # Mostrar mensaje inicial
        oled.text("Boot Menu", 0, 10, fill="white")
        oled.text("Raspberry Pi", 0, 30, fill="white")
        oled.show()
        
        print("✅ OLED conectado correctamente")
        tiene_oled = True
        
    except Exception as e:
        print(f"⚠️  OLED no disponible: {e}")
        print("⚠️  Continuando solo en terminal...")
        tiene_oled = False
        oled = None
    
    # MENU PRINCIPAL
    while running:
        print("\n" + "-" * 30)
        print("OPCIONES:")
        print("1. Ver estado del sistema")
        print("2. Reiniciar servicios")
        print("3. Apagar Raspberry")
        print("4. Salir")
        print("-" * 30)
        
        opcion = input("Selecciona una opción (1-4): ").strip()
        
        if opcion == "1":
            mensaje = "Estado del sistema"
            print("📊 Mostrando estado...")
            # Aquí tu lógica
            
        elif opcion == "2":
            mensaje = "Reiniciando servicios"
            print("🔄 Reiniciando...")
            # Tu lógica aquí
            
        elif opcion == "3":
            mensaje = "Apagando..."
            print("⏻  Apagando Raspberry Pi en 3 segundos...")
            if tiene_oled:
                oled.clear()
                oled.text("Apagando...", 0, 30, fill="white")
                oled.show()
            time.sleep(3)
            import os
            os.system("sudo shutdown -h now")
            break
            
        elif opcion == "4":
            print("Saliendo del programa...")
            break
            
        else:
            mensaje = "Opcion invalida"
            print("❌ Opción no válida")
        
        # Actualizar OLED si existe
        if tiene_oled and oled:
            try:
                oled.clear()
                oled.text(mensaje[:16], 0, 20, fill="white")
                oled.show()
            except:
                pass
        
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\n\nPrograma interrumpido por el usuario")

except Exception as e:
    print(f"\n❌ ERROR crítico: {e}")

finally:
    # LIMPIEZA FINAL (IMPORTANTE)
    print("\n🧹 Limpiando recursos...")
    try:
        if 'oled' in locals() and oled:
            oled.clear()
            oled.hide()
    except:
        pass
    
    # Forzar limpieza del bus I2C
    import subprocess
    subprocess.run(["sudo", "i2cdetect", "-y", "1", "-q"], 
                  timeout=2, 
                  capture_output=True)
    
    print("✅ Recursos liberados. Hasta luego!")
