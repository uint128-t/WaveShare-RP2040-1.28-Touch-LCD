from . import *
import displayio,terminalio,cst816,gc9a01
from adafruit_button import Button
from adafruit_display_text import label

name = "Tic Tac Toe"
def enter(disp,touch):
    root = disp.root_group
    m = label.Label(terminalio.FONT,text="Hello\nWorld",scale=2,color=0xFFFFFF)
    m.anchored_position = (120,120)
    m.anchor_point = (0.5,0.5)
    cells = []
    for i in range(9):
        btn = Button(x=(i%3)*50+70,y=(i//3)*50+70,width=70,height=70,label_font=terminalio.FONT,label=str(i),color=0xff0000)
        btn.x = (i%3)*50+70
        btn.y = (i//3)*50+70
        cells.append(btn)
        root.append(btn)
    root.append(m)
    
    while True:
        point = touch.get_point()
        gesture = touch.get_gesture()
        press = touch.get_touch()
        distance = touch.get_distance()
        if gesture==12:
            break