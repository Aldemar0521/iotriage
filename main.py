#------------------------------ [IMPORT]------------------------------------
from machine import Pin, Timer, SoftI2C, RTC
from utime import sleep_ms, localtime, sleep
import ufirebase as firebase
import wifi, heart_max, triage, mfrc522, mlx90614, time, ntptime
import database as d
import ssd1306
from screen_msg import imprimir

#------------------ [INICIALIZACION DE OBJETOS]-------------------------

## sensor RFID RC522
rfid = mfrc522.MFRC522(14, 13, 12, 27,26)

## sensor mlx90614 temperatura
i2c = SoftI2C(scl=Pin(33), sda=Pin(25), freq=80000)
sensor_temp = mlx90614.MLX90614(i2c)

## pantalla oled
pinesI2C = SoftI2C(Pin(21), Pin(18))
oled = ssd1306.SSD1306_I2C(128, 64, pinesI2C)

## Red Wi-Fi
miwifi = wifi.WIFI("HDHELA", "HHL11JA1108ah*")
miwifi.conectar()

#--------------------------- [DECLARACION FUNCIONES]---------------------------------------


def get_formattedtime():
    mytime = localtime()
    return f"{mytime[2]}/{mytime[1]}/{mytime[0]} {mytime[3]}:{mytime[4]}:{mytime[5]}"

def get_timestamp():
    mytime = localtime()
    return f"{mytime[2]}{mytime[1]}{mytime[0]}{mytime[3]}{mytime[4]}{mytime[5]}"


#---------------------- [SINCRONIZACION HORA]--------------------------------

ntptime.host = "0.south-america.pool.ntp.org"

if time.mktime(time.localtime(time.time())) == ntptime.time(): ##si localtime = a utc time, configurar utc -5
    (year, month, mday, weekday, hour, minute, second, milisecond) = RTC().datetime()
    RTC().init((year, month, mday, weekday, hour-5, minute, second, milisecond))
elif time.mktime(time.localtime(time.time())) < 112032499: ## Si localtime cerca a hora 0, ajustar a utc -5
    ntptime.settime()
    (year, month, mday, weekday, hour, minute, second, milisecond) = RTC().datetime()
    RTC().init((year, month, mday, weekday, hour-5, minute, second, milisecond))
elif ntptime.time() - 18000 == time.time():##si localtime es igual a utc time -5 no hacer nada
    pass
else:
    print(get_formattedtime())

#--------------------------- [EJECUCIÓN DE CÓDIGO]---------------------------------------


##Bucle de ejecución principal del módulo
while True:
    imprimir("Acerque su carnet al lector", 5)
    print("Acerque su carnet al lector ...")
    ##Bucle para leer continuamente el identificador de la tarjeta de acceso
    while True:
        numTarjeta = rfid.getCardValue()
        if numTarjeta == "":
            sleep(0.5)
            continue
        else:
            break
        break
    
    print("Carnet leído exitosamente")
    
    
    imprimir("Carnet leido", 5)
    
    
    inicio = time.time()
   
    try:
        ## Realizar busqueda de paciente en bd mediante # de tarjeta
        d.buscarPaciente(numTarjeta)
        ## Se pausa el ciclo de ejecución para mostrar los datos de usuario en pantalla
        sleep(5)
        
        ##Se imprime instruccion a usuario en pantalla oled
        print("Ubique su rostro en frente del sensor de temperatura\n")
        imprimir("Ubique rostro en frente del sensor de temperatura", 5)
        sleep(4)
        print("Tomando temperatura, no se retire\n")
        imprimir("Tomando temperatura", 5)
        ## Toma lectura de temperatura
        temperatura = float("{0:.2f}".format(sensor_temp.read_object_temp()))
        
        ##Se muestra temperatura obtenida en pantalla oled
        print("Temperatura:", temperatura, "°C")
        imprimir(f"Temperatura: {temperatura}", 25,0,0)
        sleep(4)
        
        ##Se imprime instruccion a usuario en pantalla oled
        print("Ubique el dedo indice en el sensor y espere 10 segundos")
        imprimir(f"Ubique dedo en sensor cardiaco por 10 segundos", 5)
        sleep(4)
        
        ##Lectura de signos, calculo de ritmo cardiaco, calculo de saturacion oxigeno
        heart_max.leer_signos()
        heart_max.calcular_ritmo()
        heart_max.calcular_saturacion()
        
        ##Se imprime informacion cardiaca en pantalla oled
        imprimir("Ritmo: "+str(heart_max.bpm),5)
        imprimir("Saturacion: "+str(float("{0:.2f}".format(heart_max.saturacion))),25,0,0)
        sleep(4)
        
        ##Registrar signos vitales en bd
        d.subirSignosVitales(d.cedula, d.fechaId, d.fechaForm, heart_max.saturacion, temperatura, heart_max.bpm)
        ##Instanciación datos triaje
        datostriage = triage.TRIAGE(d.cedula, d.fechaId, d.fechaForm, heart_max.bpm, heart_max.saturacion, temperatura)
        ##Llamar método hacerTriage()
        datostriage.hacerTriage()
        
        fin = time.time()
        sleep(5)
        print(f"Tiempo total proceso: {fin-inicio} segundos.")
  
    except AttributeError as e:
        print("Paciente no encontrado en el sistema.\n")
        imprimir(f"Paciente no encontrado en el sistema", 5)


##impresiones en oled
##database
##triage
##main

