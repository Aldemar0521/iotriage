import ufirebase as firebase
from utime import localtime
from screen_msg import imprimir

firebase.setURL("https://triage-automatizado-default-rtdb.firebaseio.com/")


def get_formattedtime():
    mytime = localtime()
    return f"{mytime[2]}/{mytime[1]}/{mytime[0]} {mytime[3]}:{mytime[4]}:{mytime[5]}"

def get_timestamp():
    mytime = localtime()
    return f"{mytime[2]}{mytime[1]}{mytime[0]}{mytime[3]}{mytime[4]}{mytime[5]}"


cedula = 0
fechaId = ""
fechaForm = ""


def buscarPaciente(numTarjeta):
    
    firebase.get(f"tarjetas/{numTarjeta}", "tarjetas", bg=0)
    global cedula
    cedula = firebase.tarjetas.get("paciente")
    firebase.get(f"pacientes/{cedula}", "pacientes", bg=0)
    #diccionario que contiene el paciente consultado
    paciente = firebase.pacientes
    cedula = paciente["cedula"]
    nombrePac = paciente["nombre"]
    apellidoPac = paciente["apellidos"]
    global fechaId
    fechaId = get_timestamp()
    global fechaForm
    fechaForm = get_formattedtime()
    
    print("**Datos paciente:**\n", "\nNombre: ", nombrePac, "\nApellidos: ", apellidoPac,
          "\nCedula: ", cedula)


    imprimir("Paciente", 5,0,1)
    imprimir("Nombre:"+nombrePac, 15,0,0)
    imprimir("Apellido:"+apellidoPac, 25,0,0)
    imprimir("Cedula:"+str(cedula), 35,0,0)
    
    
    return (cedula, fechaId, fechaForm)
        

def subirSignosVitales(cedula, fechaId, fechaForm, saturacion, temperatura, ritmo):
    firebase.put(f"signos_vitales/{cedula}/{fechaId}", {"fecha_muestra": fechaForm, "ritmo": ritmo, "saturacion": saturacion, "temperatura": temperatura}, bg=0)
    
    
# import wifi
# miwifi = wifi.WIFI("HDHELA", "HHL11JA1108ah*")
# miwifi.conectar()
# buscarPaciente('0x2a7303d0')
    
    