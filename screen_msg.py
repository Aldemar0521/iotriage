import ssd1306
from time import sleep
from machine import SoftI2C, Pin


pinesI2C = SoftI2C(Pin(21), Pin(18))
oled = ssd1306.SSD1306_I2C(128, 64, pinesI2C)


def imprimir(texto, yinicio, xinicio=0, borrar=1):
    if borrar == 1:
        oled.fill(0)
        oled.show()
        ylimit = 16
        while len(texto) > ylimit:
            oled.text(texto[0:ylimit+1], 0, yinicio)
            oled.show()
            yinicio += 10
            texto = texto[ylimit:]
            if texto[0].isspace():
                texto = texto[1:]
        oled.text(texto, 0, yinicio)
        oled.show()
    else:
        ylimit = 16
        while len(texto) > ylimit:
            oled.text(texto[0:ylimit+1], 0, yinicio)
            oled.show()
            yinicio += 10
            texto = texto[ylimit:]
            if texto[0].isspace():
                texto = texto[1:]
        oled.text(texto, 0, yinicio)
        oled.show()
 
 
