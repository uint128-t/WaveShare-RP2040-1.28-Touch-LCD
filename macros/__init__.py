from . import *
import os
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import usb_hid,supervisor
from time import sleep

macros = []
disabled = False

if not supervisor.runtime.usb_connected: # Cable does not support data/No data from host
    print("Not connected to host, cannot use macros!") # Fix hangs
    kbd = None
    layout = None
    disabled = True
else:
    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)

for module in os.listdir("/macros"):
    if module == "__init__.py" or module[-3:] != ".py":
        continue
    print(f"load macro {module}")
    exec(f"from . import {module[:-3]} as prgm") # fun
    prgm.id = module[:-3]
    macros.append(prgm)

print(macros)