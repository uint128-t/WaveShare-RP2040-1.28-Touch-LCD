from . import *
import displayio,terminalio,cst816,gc9a01
from adafruit_button import Button
from adafruit_display_text import label

name = "Hello World"
root = displayio.Group()
m = label.Label(terminalio.FONT,text="Hello\nWorld",scale=2,color=0x00FFFF)
m.anchored_position = (120,120)
m.anchor_point = (0.5,0.5)
root.append(m)
def enter(disp,touch):
    disp.root_group = root
    while True:
        point = touch.get_point()
        gesture = touch.get_gesture()
        press = touch.get_touch()
        distance = touch.get_distance()
        if gesture==12:
            break