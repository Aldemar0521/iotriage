# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import wifi

miwifi = wifi.WIFI("HDHELA", "HHL11JA1108ah*")
miwifi.conectar()