from . import *

name = "Test"
def enter():
    kbd.send(Keycode.WINDOWS, Keycode.R)
    sleep(0.1)
    layout.write("msg %username% This is a message.")
    kbd.send(Keycode.ENTER)