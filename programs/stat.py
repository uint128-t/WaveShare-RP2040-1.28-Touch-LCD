from . import *
import displayio,terminalio,board,microcontroller,gc,time
from adafruit_display_text import label

name = "Statistics"

def enter(disp,touch):
    root = disp.root_group
    m = label.Label(terminalio.FONT,text="Please wait",scale=1,color=0x00FFFF)
    m.x = 0
    m.y = 65
    root.append(m)
    while True:
        point = touch.get_point()
        gesture = touch.get_gesture()
        press = touch.get_touch()
        distance = touch.get_distance()
        text = f"""\
    Chip: {os.uname().sysname}
   CPy Ver: {os.uname().release}
 Memory: {gc.mem_alloc()} USED {gc.mem_free()} FREE
ID: {board.board_id}
{os.uname().machine}
 UID: {bytes(microcontroller.cpu.uid)}
  CPU Freq: {microcontroller.cpu.frequency/1024/1024} MHz
   CPU Temp: {microcontroller.cpu.temperature} C\
"""
        m.text = text
        if gesture==12:
            break
        time.sleep(0.5)