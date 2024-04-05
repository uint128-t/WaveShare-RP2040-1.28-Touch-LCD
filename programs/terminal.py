from . import *
import displayio,terminalio,cst816,gc9a01
from adafruit_button import Button
from adafruit_display_text import label

name = "CircuitPython Terminal"
def enter(disp,touch):
    root = disp.root_group
    root.append(displayio.CIRCUITPYTHON_TERMINAL)
    root.y = 0
    while True:
        point = touch.get_point()
        gesture = touch.get_gesture()
        press = touch.get_touch()
        distance = touch.get_distance()
        if gesture==12:
            break
        if press and (gesture==1 or gesture==2):
            disp.root_group.y+=distance.y_dist
    root.pop()