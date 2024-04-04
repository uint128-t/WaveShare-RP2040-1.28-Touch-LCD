import displayio,board,terminalio,digitalio,macros
from adafruit_button import Button
from adafruit_display_text import label

name="Macros"

def enter(disp,touch):
    main = disp.root_group
    m = label.Label(terminalio.FONT,text="Macros",scale=2,color=0xFF00FF)
    m.anchored_position = (120,15)
    m.anchor_point = (0.5,0)
    main.append(m)
    ra = label.Label(terminalio.FONT,text=">",color=0xFF0000)
    ra.anchored_position = (20,120)
    ra.anchor_point = 0,0.5
    main.append(ra)

    listg = displayio.Group()
    main.append(listg)

    b = Button(x=80,y=190,width=40,height=30,name="X",label="Run",label_font=terminalio.FONT,label_color=0xFFFFFF,outline_color=0x00AAFF,fill_color=0)
    main.append(b)
    c = Button(x=120,y=190,width=40,height=30,name="X",label="Close",label_font=terminalio.FONT,label_color=0xFFFFFF,outline_color=0x00AAFF,fill_color=0)
    main.append(c)

    plist = []
    sel = None
    abp = 0
    for i,program in enumerate(macros.macros):
        l = label.Label(terminalio.FONT,text=f"{program.id}: {program.name}") # color,scale
        l.y = 60+i*10
        l.x = 40
        listg.append(l)
        plist.append(l)
    sele = None
    while True:
        point = touch.get_point()
        gesture = touch.get_gesture()
        press = touch.get_touch()
        distance = touch.get_distance()
        if press and (gesture==1 or gesture==2):
            listg.y+=distance.y_dist
            abp+=distance.y_dist
            for pr,p in zip(macros.macros,plist):
                if p.y+abp>=115 and p.y+abp<125:
                    p.color = 0x00FF00
                    sel = pr
                    sele = p
                else:
                    p.color = 0xFFFFFF

        if press and gesture==0 and b.contains((point.x_point,point.y_point)) and sel is not None:
            sele.color=0x00AAFF
            sel.enter()
        if press and gesture==0 and c.contains((point.x_point,point.y_point)):
            gst = 0
            while gst==0:
                gst=touch.get_gesture()
            return