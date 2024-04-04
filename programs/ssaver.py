from . import *
import displayio,terminalio,colorsys
from adafruit_button import Button
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from time import monotonic

name = "Screensaver"
def enter(disp,touch):
    root = displayio.Group()
    rect = Rect(0,0,240,30,fill=0x0000FF)
    root.append(rect)
    disp.root_group = root
    while True:
        rect.y+=1
        rect.y%=240
        color = colorsys.hsv_to_rgb(monotonic()%1,1,1)
        rect.fill = (int(color[0]*255)<<16)+(int(color[1]*255)<<8)+int(color[2]*255)
        point = touch.get_point()
        gesture = touch.get_gesture()
        press = touch.get_touch()
        distance = touch.get_distance()
        if gesture==12:
            break