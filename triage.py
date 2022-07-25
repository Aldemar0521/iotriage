import ufirebase as firebase
from screen_msg import imprimir
import urequests


firebase.setURL("https://triage-automatizado-default-rtdb.firebaseio.com/")
ifttturl = "https://maker.ifttt.com/trigger/inform_triages/with/key/dCZmYv7EIlhk_knsTPlc-I?"


class TRIAGE:
    
    def __init__(self, cedula, fechaid, fecha, ritmo, saturacion, temperatura):
        self.cedula = cedula
        self.fechaid = fechaid
        self.fecha = fecha
        self.ritmo = ritmo
        self.saturacion = saturacion
        self.temperatura = temperatura
        
    def hacerTriage(self):
        firebase.get(f"signos_vitales/{self.cedula}/{self.fechaid}", "signos", bg=0)
        self.ritmo = firebase.signos.get("ritmo")
        print("\n**Triage realizado: A continuación los detalles**")
        if self.ritmo > 110 and self.saturacion < 88:
            firebase.put(f"triage/{self.cedula}{self.fechaid}", {"fecha_triage": self.fecha, "paciente": self.cedula, "prioridad": 1, "signos_vitales": self.fechaid}, bg=0)
            print(f"Signos vitales: Ritmo cardiaco: {self.ritmo}, Saturación Oxígeno: {self.saturacion}, Temperatura: {self.temperatura}")
            print("Prioridad 1: Elevado ritmo cardiaco y baja saturación")
            
            imprimir("Prioridad 1: Elevado ritmo cardiaco y baja saturacion",10)
        elif 100 <= self.ritmo <= 110 and 88 <= self.saturacion <= 90:
            firebase.put(f"triage/{self.cedula}{self.fechaid}", {"fecha_triage": self.fecha, "paciente": self.cedula, "prioridad": 2, "signos_vitales": self.fechaid}, bg=0)
            print("Prioridad 2: Alto ritmo cardiaco y saturación moderada")
            print(f"Signos vitales: Ritmo cardiaco: {self.ritmo}, Saturación Oxígeno: {self.saturacion}, Temperatura: {self.temperatura}")
            
            imprimir("Prioridad 2: Alto ritmo cardiaco y saturacion moderada",10)
        elif 81 <= self.ritmo  <= 99 and 88 <= self.saturacion <= 90:
            firebase.put(f"triage/{self.cedula}{self.fechaid}", {"fecha_triage": self.fecha, "paciente": self.cedula, "prioridad": 4, "signos_vitales": self.fechaid}, bg=0)
            print("Prioridad 4: Ritmo cardiaco medio y saturación moderada")
            print(f"Signos vitales: Ritmo cardiaco: {self.ritmo}, Saturación Oxígeno: {self.saturacion}, Temperatura: {self.temperatura}")
            
            imprimir("Prioridad 4: Ritmo cardiaco medio y saturacion moderada", 10)
        elif 81 <= self.ritmo  <= 99 and self.saturacion > 90 and self.temperatura <= 34.5:
            firebase.put(f"triage/{self.cedula}{self.fechaid}", {"fecha_triage": self.fecha, "paciente": self.cedula, "prioridad": 1, "signos_vitales": self.fechaid}, bg=0)
            print("Prioridad 1: Ritmo cardiaco medio, saturación adecuada y temperatura baja")
            print(f"Signos vitales: Ritmo cardiaco: {self.ritmo}, Saturación Oxígeno: {self.saturacion}, Temperatura: {self.temperatura}")
            
            imprimir("Prioridad 1: Ritmo cardiaco medio, saturacion adecuada y temperatura baja",10)
        elif 81 <= self.ritmo  <= 99 and self.saturacion > 90:
            firebase.put(f"triage/{self.cedula}{self.fechaid}", {"fecha_triage": self.fecha, "paciente": self.cedula, "prioridad": 4, "signos_vitales": self.fechaid}, bg=0)
            print("Prioridad 4: Ritmo cardiaco medio y saturación adecuada")
            print(f"Signos vitales: Ritmo cardiaco: {self.ritmo}, Saturación Oxígeno: {self.saturacion}, Temperatura: {self.temperatura}")
            
            imprimir("Prioridad 4: Ritmo cardiaco medio y saturacion adecuada",10)
        elif 50 <= self.ritmo  <= 80 and 84 <= self.saturacion <= 88:
            firebase.put(f"triage/{self.cedula}{self.fechaid}", {"fecha_triage": self.fecha, "paciente": self.cedula, "prioridad": 2, "signos_vitales": self.fechaid}, bg=0)
            print("Prioridad 2: Saturación baja")
            print(f"Signos vitales: Ritmo cardiaco: {self.ritmo}, Saturación Oxígeno: {self.saturacion}, Temperatura: {self.temperatura}")
            
            imprimir("Prioridad 2: Saturacion baja",10)
        elif self.saturacion < 85:
            firebase.put(f"triage/{self.cedula}{self.fechaid}", {"fecha_triage": self.fecha, "paciente": self.cedula, "prioridad": 1, "signos_vitales": self.fechaid}, bg=0)
            print("Prioridad 1: Saturación extremadamente baja")
            print(f"Signos vitales: Ritmo cardiaco: {self.ritmo}, Saturación Oxígeno: {self.saturacion}, Temperatura: {self.temperatura}")
            
            imprimir("Prioridad 1: Saturacion extremadamente baja",10)
        elif 38.1 <= self.temperatura <= 38.6:
            firebase.put(f"triage/{self.cedula}{self.fechaid}", {"fecha_triage": self.fecha, "paciente": self.cedula, "prioridad": 2, "signos_vitales": self.fechaid}, bg=0)
            print("Prioridad 2: Fiebre alta")
            print(f"Signos vitales: Ritmo cardiaco: {self.ritmo}, Saturación Oxígeno: {self.saturacion}, Temperatura: {self.temperatura}")
            
            imprimir("Prioridad 2: Fiebre alta",10)
        elif self.temperatura > 38.6:
            firebase.put(f"triage/{self.cedula}{self.fechaid}", {"fecha_triage": self.fecha, "paciente": self.cedula, "prioridad": 1, "signos_vitales": self.fechaid}, bg=0)
            print("Prioridad 1: Fiebre extremadamente alta")
            print(f"Signos vitales: Ritmo cardiaco: {self.ritmo}, Saturación Oxígeno: {self.saturacion}, Temperatura: {self.temperatura}")
            
            imprimir("Prioridad 1: Fiebre extremadamente alta",10)
        elif 37.5 <= self.temperatura <= 38:
            firebase.put(f"triage/{self.cedula}{self.fechaid}", {"fecha_triage": self.fecha, "paciente": self.cedula, "prioridad": 4, "signos_vitales": self.fechaid}, bg=0)
            print("Prioridad 4: Febrícula")
            print(f"Signos vitales: Ritmo cardiaco: {self.ritmo}, Saturación Oxígeno: {self.saturacion}, Temperatura: {self.temperatura}")
            
            imprimir("Prioridad 4: Febrícula",10)
        elif 35 <= self.temperatura <= 35.5:
            firebase.put(f"triage/{self.cedula}{self.fechaid}", {"fecha_triage": self.fecha, "paciente": self.cedula, "prioridad": 2, "signos_vitales": self.fechaid}, bg=0)
            print("Prioridad 2: Temperatura baja")
            print(f"Signos vitales: Ritmo cardiaco: {self.ritmo}, Saturación Oxígeno: {self.saturacion}, Temperatura: {self.temperatura}")
            
            imprimir("Prioridad 2: Temperatura baja",10)
        elif self.temperatura < 35:
            firebase.put(f"triage/{self.cedula}{self.fechaid}", {"fecha_triage": self.fecha, "paciente": self.cedula, "prioridad": 1, "signos_vitales": self.fechaid}, bg=0)
            print("Prioridad 1: Temperatura extremadamente baja")
            print(f"Signos vitales: Ritmo cardiaco: {self.ritmo}, Saturación Oxígeno: {self.saturacion}, Temperatura: {self.temperatura}")
            
            imprimir("Prioridad 1: Temperatura extremadamente baja",10)
        elif self.ritmo < 45:
            firebase.put(f"triage/{self.cedula}{self.fechaid}", {"fecha_triage": self.fecha, "paciente": self.cedula, "prioridad": 1, "signos_vitales": self.fechaid}, bg=0)
            print("Prioridad 1: Ritmo cardiaco bajo")
            print(f"Signos vitales: Ritmo cardiaco: {self.ritmo}, Saturación Oxígeno: {self.saturacion}, Temperatura: {self.temperatura}")
            
            imprimir("Prioridad 1: Ritmo cardiaco bajo",10)
        else:
            firebase.put(f"triage/{self.cedula}{self.fechaid}", {"fecha_triage": self.fecha, "paciente": self.cedula, "prioridad": 5, "signos_vitales": self.fechaid}, bg=0)
            print("Prioridad 5: No se encuentra dentro de las condiciones de urgencia mayor.")
            print(f"Signos vitales: Ritmo cardiaco: {self.ritmo}, Saturación Oxígeno: {self.saturacion}, Temperatura: {self.temperatura}")
            
            imprimir("Prioridad 5: No se encuentra dentro de las condiciones de urgencia mayor.",10)
        