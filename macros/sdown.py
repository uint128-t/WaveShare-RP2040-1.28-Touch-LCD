from . import *

name = "Shutdown"
def enter():
    kbd.send(Keycode.WINDOWS, Keycode.X)
    layout.write("uuuuuuuuuuuuuuuuuuuuuuu")