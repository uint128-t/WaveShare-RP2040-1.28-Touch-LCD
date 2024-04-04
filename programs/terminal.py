from . import *
import displayio,terminalio,cst816,gc9a01
from adafruit_button import Button
from adafruit_display_text import label

name = "CircuitPython Terminal"
def enter(disp,touch):
    disp.root_group = displayio.CIRCUITPYTHON_TERMINAL
    while True:
        point = touch.get_point()
        gesture = touch.get_gesture()
        press = touch.get_touch()
        distance = touch.get_distance()
        if gesture==12:
            break