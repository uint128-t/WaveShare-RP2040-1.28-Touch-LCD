from . import *
import displayio,terminalio,board,microcontroller,gc,time,busio,displ
from adafruit_display_text import label
import jepstone_qmi8658

name = "Accel/Gyro"

def enter(disp,touch):
    root = disp.root_group
    m = label.Label(terminalio.FONT,text="Please wait",scale=1,color=0xFFFFFF)
    m.x = 0
    m.y = 100
    root.append(m)
    device = jepstone_qmi8658.QMI8658(displ.i2c)
    while True:
        point = touch.get_point()
        gesture = touch.get_gesture()
        press = touch.get_touch()
        distance = touch.get_distance()
        text = f"""\
Accel: {device.acceleration}
Gyro: {device.gyro}
Temperature: {device.temperature}\
\
"""
        m.text = text
        if gesture==12:
            break
        time.sleep(0.5)