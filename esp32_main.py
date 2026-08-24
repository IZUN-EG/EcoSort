import machine
import uselect
import time
import sys

servo1 = machine.PWM(machine.Pin(23), freq=50)
servo2 = machine.PWM(machine.Pin(22), freq=50)
servo3 = machine.PWM(machine.Pin(21), freq=50)
servo4 = machine.PWM(machine.Pin(19), freq=50)

servo1.duty(45)
servo2.duty(45)
servo3.duty(45)
servo4.duty(45)


def mover_compuerta():

    print("MOVIENDO: COMPUERTA")

    servo4.duty(120)
    time.sleep(1)
    servo4.duty(45)
    time.sleep(1)

    

    print("LISTO: COMPUERTA")
    

def mover_plastico():
    print("MOVIENDO:PLASTICO")
    servo1.duty(120)
    time.sleep(1)
    mover_compuerta()
    servo1.duty(45)
    time.sleep(1)

    
    print("LISTO: PLASTICO")
    
def open_plastico():
    print("OPEN:PLASTICO")
    servo1.duty(120)
    time.sleep(1)
    
def close_plastico():
    print("CLOSE:PLASTICO")
    servo1.duty(45)
    time.sleep(1)
    
    
def mover_metal():
    print("MOVIENDO:METAL")
    
    servo2.duty(120)
    time.sleep(1)
    open_plastico()
    mover_compuerta()
    close_plastico()
    servo2.duty(45)
    time.sleep(1)

    
    print("LISTO: METAL")
    
def open_metal():
    print("OPEN:METAL")
    servo2.duty(120)
    time.sleep(1)
    
def close_metal():
    print("CLOSE:METAL")
    servo2.duty(45)
    time.sleep(1)   
    print("LISTO: METAL")
    
    
def mover_papel():
    print("MOVIENDO:PAPEL")
    
    servo3.duty(120)
    time.sleep(1)
    open_plastico()
    open_metal()
    mover_compuerta()
    close_metal()
    close_plastico()
    servo3.duty(45)
    time.sleep(1)

    print("LISTO: PAPEL")
    



poll = uselect.poll()
poll.register(
    sys.stdin,
    uselect.POLLIN
)

print("READY")

while True:
    
    events = poll.poll(100)
    
    if events:
        command = sys.stdin.readline().strip()
        
        if command == "":
            continue
        
        if command == "PLASTICO":
            print("RECIBIDO: PLASTICO")
            
            mover_plastico()
            
            print("OK:PLASTICO")
            
            
        elif command == "METAL":
            
            print("RECIBIDO: METAL")
            
            mover_metal()
            
            print("OK:METAL")
            
        elif command == "PAPEL":
            print("RECIBIDO: PAPEL")
            
            mover_papel()
            
            print("OK:PAPEL")
            
        elif command == "ERROR":
            
            print("RECIBIDO: SERVO4")
            
            mover_compuerta()
            
            print("OK:COMPUERTA")
            
        elif command == "STOP":
            print("RECIBIDO: STOP")
            
            servo1.duty(45)
            servo2.duty(45)
            servo3.duty(45)
            servo4.duty(45)
            
            print("OK:STOP")
        
        else:
            print("ERROR: COMANDO DESCONOCIDO")
    
if servo == 1:
    mover_plastico()

   # servo1.duty(45)
   # time.sleep(2)
elif servo == 2:
    mover_metal()

   # servo2.duty(44)
   # time.sleep(2)
elif servo == 3:
    mover_papel()

   # servo3.duty(48)
    #time.sleep(2)
elif servo == 4:
    mover_servo4()
    #servo4.duty(45)
    #time.sleep(2)
    
else:
    print("No se eligio un motor valido")
    
servo1.deinit()
servo2.deinit()
servo3.deinit()
servo4.deinit()
