from time import sleep
import network


class WIFI:
    
    def __init__(self, SSID, pwd):
        self.SSID = SSID
        self.pwd = pwd
    
    def conectar(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('Conectando a red Wi-Fi ...')
            try:
                wlan.connect(self.SSID, self.pwd)
            except OSError:
                print("No se puede conectar a la red Wi-Fi.")
        else:
            print("Ya está conectado.")
        print(f"Conectado a: {self.SSID}")
        print(f"Configuración de red: {wlan.ifconfig()}")
        
    def chequear(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if wlan.isconnected():
            return True
        else:
            return False
