import displayio,board,terminalio,busio,digitalio,gc9a01,programs,cst816
from adafruit_button import Button
from adafruit_display_text import label
from displ import * # I want to use the variables but don't rerun the code??

main = displayio.Group()
display.root_group = main

listg = displayio.Group()

# load UI

m = label.Label(terminalio.FONT,text="Programs",scale=2,color=0x0000FF)
m.anchored_position = (120,15)
m.anchor_point = (0.5,0)
main.append(m)
ra = label.Label(terminalio.FONT,text=">",color=0xFF0000)
ra.anchored_position = (20,120)
ra.anchor_point = 0,0.5
main.append(ra)
main.append(listg)

b = Button(x=80,y=190,width=80,height=30,name="X",label="Run",label_font=terminalio.FONT,label_color=0xFFFFFF,outline_color=0x00AAFF,fill_color=0)
main.append(b)

plist = []
sel = None
sele = None
abp = 0
for i,program in enumerate(programs.programs):
    l = label.Label(terminalio.FONT,text=f"{program.id}: {program.name}") # color,scale
    l.y = 60+i*10
    l.x = 40
    listg.append(l)
    plist.append(l)
    
while True:
    point = touch.get_point()
    gesture = touch.get_gesture()
    press = touch.get_touch()
    distance = touch.get_distance()
    if press and (gesture==1 or gesture==2):
        listg.y+=distance.y_dist
        abp+=distance.y_dist
        for pr,p in zip(programs.programs,plist):
            if p.y+abp>=115 and p.y+abp<125:
                p.color = 0x00FF00
                sel = pr
                sele = p
            else:
                p.color = 0xFFFFFF
    

    if press and gesture==0 and b.contains((point.x_point,point.y_point)) and sel is not None:
        print(f"Open program {sel}")
        sele.color=0x00AAFF
        gst = 0
        while gst==0:
            gst=touch.get_gesture()
        display.root_group = displayio.Group()
        sel.enter(display,touch) # program mainloop
        display.root_group = main
    # print("Position: {0},{1} - Gesture: {2} - Pressed? {3} - Distance: {4},{5}".format(point.x_point, point.y_point, gesture, press, distance.x_dist, distance.y_dist))