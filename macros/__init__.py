from . import *
import os
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from time import sleep
import usb_hid

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

macros = []
print("Loading macros...")
for module in os.listdir("/macros"):
    if module == "__init__.py" or module[-3:] != ".py":
        continue
    print(f"load macro {module}")
    exec(f"from . import {module[:-3]} as prgm") # fun
    prgm.id = module[:-3]
    macros.append(prgm)

print(macros)