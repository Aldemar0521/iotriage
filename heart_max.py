from max30102 import MAX30102

from machine import sleep, SoftI2C, Pin
from utime import ticks_diff, ticks_us
from time import time, sleep

from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM

i2c = SoftI2C(sda=Pin(4),  # Here, use your I2C SDA pin
              scl=Pin(5),  # Here, use your I2C SCL pin
              freq=400000)  # Fast: 400kHz, slow: 100kHz


sensor = MAX30102(i2c=i2c)  # An I2C instance is required


if sensor.i2c_address not in i2c.scan():
    print("Sensor not found.")
elif not (sensor.check_part_id()):

    print("I2C device ID not corresponding to MAX30102 or MAX30105.")
else:
    print("Sensor connected and recognized.")


print("Setting up sensor with default configuration.", '\n')
sensor.setup_sensor()



sleep(1)

print("Iniciando lectura de datos", '\n')

sleep(1)


#Lista para almacenar datos de sensor led rojo (ritmo cardiaco)
redlist = []
#Lista para almacenar datos de sensor led infrarrojo (saturación de oxigeno)
irlist = []

bpm = 0
saturacion = 0


storage = 0
def leer_signos():

    listsize = 501
    
    global redlist, irlist
    redlist.clear()
    irlist.clear()

    while storage < listsize:
        
        sensor.check()    
            
        if sensor.available():
            red_reading = sensor.pop_red_from_storage()
            ir_reading = sensor.pop_ir_from_storage()
            global redlist, irlist
            redlist.append(red_reading)
            irlist.append(ir_reading)
            
            global storage
            storage += 1

            
            ##Para debug o graficar ir
#             if ir_reading < 12500 and red_reading < 14000:
#                 pass
#             else:
#                 print(ir_reading, red_reading) 


        ## para debug y graficar red
#             if red_reading < 14000:
#                 pass
#             else:
#                 print(red_reading)
                
    
    
    
    
    ##Eliminar la primera lectura, la cual siempre es errónea con el módulo empleado
    print("Done reading")
    global redlist, irlist
    redlist.pop(0)
    irlist.pop(0)
    
    


def calcular_ritmo():
    global redlist, bpm
    bpm = 0
    prom = sum(redlist)/len(redlist)
    
    diffv3 = (max(redlist)-min(redlist))*0.1
    
    bp10 = 0
    global redlist
    
    for x in range(len(redlist)):
        if x == 0:
            global redlist
            if redlist[x] > redlist[x+1] and redlist[x] > redlist[x+2] and redlist[x] > redlist[x+3]:
                bp10 += 1

            else:
                pass
        elif x == 1:
            global redlist
            if redlist[x] > redlist[x-1] and redlist[x] > redlist[x+1] and redlist[x] > redlist[x+2] and redlist[x] > redlist[x+3]:
                bp10 += 1

            else:
                pass
        
        elif x == 2:
            global redlist
            if redlist[x] > redlist[x-2] and redlist[x] > redlist[x-1] and redlist[x] > redlist[x+1] and redlist[x] > redlist[x+2] and redlist[x] > redlist[x+3]:
                bp10 += 1

            else:
                pass
        
        elif x == 3:
            global redlist
            if redlist[x] > redlist[x-3] and redlist[x] > redlist[x-2] and redlist[x] > redlist[x-1] and redlist[x] > redlist[x+1] and redlist[x] > redlist[x+2] and redlist[x] > redlist[x+3]:
                bp10 += 1

            else:
                pass
            

        elif 3 < x < len(redlist)-3:
            if redlist[x] > redlist[x-3] and redlist[x] > redlist[x-2] and redlist[x] > redlist[x-1] and redlist[x] > redlist[x+1] and redlist[x] > redlist[x+2] and redlist[x] > redlist[x+3]:
                bp10 += 1
            else:
                pass
                
    print(f"Pulsaciones 10 segundos: {bp10}")
    print(f"Pulsaciones por minuto: {bp10*6}")
#     print(redlist)
#     print(debugbeats)
#     print(f"min: {min(redlist)}")
#     print(f"min: {max(redlist)}")    
#     print(f"diff: {max(redlist)-min(redlist)}")
#     print(f"prom: {prom}")
#     print(f"cont >: {prom + diffv3}")
    
    global bpm
    bpm = bp10 * 6
#     return bpm
            
            


def calcular_saturacion():
    
    global irlist, saturacion
    saturacion = 0
    max_saturacion = 13618
    
    prom1 = sum(irlist)/len(irlist)
    menor = min(irlist)
    mayor = max(irlist)
#     print(f"min: {menor}")
#     print(f"max: {mayor}")
#     print(f"diff: {mayor-menor}")
#     print(prom1)
    
    global saturacion
    saturacion = (prom1 * 100)/max_saturacion
    
#     return saturacion


    
    



        

# init = time()
# leer_signos()
# finish = time()
# 
# calcular_ritmo()
# print(f"bpm: {bpm}")
# 
# calcular_saturacion()
# print(saturacion, "% SPO2")
# 
# 
# print(f"Tiempo medición: {finish - init}")
