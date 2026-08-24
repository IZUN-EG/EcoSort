import serial
import time

esp32 = serial.Serial("COM5", 115200, timeout=1)
time.sleep(2)
print("Puerto abierto")

def enviar_residuo(clase):
    command = clase.upper()
    esp32.write((command + "\n").encode())
    print(f"Comando enviado: {command}")

    while True:
        response = esp32.readline().decode().strip()

        if response:
            print("ESP32:", response)

            if response == "OK:" + command:
                return True

            if response == "ERROR: COMANDO DESCONOCIDO":
                return False

def cerrar():
    if esp32.is_open:
        esp32.close()
        print("Puerto cerrado")