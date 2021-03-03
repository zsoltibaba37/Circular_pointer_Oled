from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
from utime import sleep_ms
import gfx
from math import sin, cos, pi

oled_width = 128
oled_height = 64

# Init Display
i2c = I2C(0,sda=Pin(0),scl=Pin(1),freq=40000)
oled = SSD1306_I2C(128,64,i2c)
graphics = gfx.GFX(oled_width, oled_height, oled.pixel)
pot = ADC(Pin(26))

def drawBorder():
    graphics.line(1,10,10,1,1)
    graphics.line(10,1,117,1,1)
    graphics.line(117,1,126,10,1)
    graphics.line(126,10,126,53,1)
    graphics.line(126,53,117,63,1)
    graphics.line(10,63,117,63,1)
    graphics.line(10,63,1,53,1)
    graphics.line(1,53,1,10,1)
    graphics.line(10,1,10,63,1)
    graphics.line(1,10,10,10,1)
    graphics.line(1,53,10,53,1)
    
#oled.invert(True)

while True:
    angle = (pot.read_u16())/20800 # 65535 / 3,1415 ~= 20861    like map() function in C++
    value = int(angle * 31.831927) # 100 / 3,1415 ~= 31.831927  0 - 100 % show value
    x = int(32 * cos(angle))
    y = int(32 * sin(angle))
    graphics.circle(64, 40, 34, 1)
    graphics.circle(64, 40, 32, 1)
    graphics.fill_circle(64, 40, 5, 1)
    graphics.fill_rect(0, 41, 128, 34, 0) # hide half circle
    oled.text("0", 20, 38, 1)
    oled.text("100", 100, 38, 1)
    oled.text("Val:", 16, 50, 1)
    drawBorder()
    graphics.line(int(oled_width / 2), int(oled_height / 2)+8, 128 - int(x + oled_width / 2), 64 - int(y + oled_height / 2)+8, 1)
    # calc x coord
    if (value < 10):
        xx = int(oled_width/2)-3
    if (value >= 10 and value < 100):
        xx = int(oled_width/2)-8
    elif (value == 100):
        xx = int(oled_width/2)-12
    graphics.fill_rect(64-15, 46, 30, 15, 1)
    oled.text(str(value), xx, 50, 0) # Value on bottom middle
    # Left Bar Graph 
    if value < 1:
        value = 1
    barValue = (52-int(angle * 13.6877))+1
    if barValue < 1:
        barValue = 1
    for i in range(4, 10, 3):
        graphics.line(i, 52, i, barValue, 1)
    # Show all
    oled.show()
    oled.fill(0)
