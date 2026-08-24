from SORTERSM import detectar_residuo
from comms_esp32 import enviar_residuo, cerrar
import time

CONFIDENCE_THRESHOLD = 80.0
WAIT_TIME = 5

print("======================================")
print("              ECOSORT")
print("======================================")
print("Iniciando sistema...\n")

detector = detectar_residuo()

try:
    while True:
        clase, confianza = next(detector)

        print("\n======================================")
        print("        RESULTADO RECIBIDO")
        print("======================================")
        print(f"Clase: {clase}")
        print(f"Confianza: {confianza:.1f}%")
        print(f"Threshold: {CONFIDENCE_THRESHOLD:.1f}%")
        print("======================================")

        if clase == "NULL":
            print("Residuo no identificado. Volviendo a analizar...")
            continue

        if confianza >= CONFIDENCE_THRESHOLD:
            print("Confianza suficiente.")
            print(f"Enviando {clase.upper()} a la ESP32...")
            enviar_residuo(clase)
            print(f"Esperando {WAIT_TIME} segundos...")
            time.sleep(WAIT_TIME)
        else:
            print(f"Confianza insuficiente ({confianza:.1f}%).")
            print("Volviendo a analizar el residuo...")

except KeyboardInterrupt:
    print("\nSistema detenido por el usuario.")
except StopIteration:
    print("\nEl detector terminó.")
except Exception as e:
    print(f"\nERROR: {e}")
finally:
    cerrar()