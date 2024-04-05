import displayio
import terminalio
import gc
from adafruit_display_text import label

x = displayio.Group()
while True:
    try:
        print(f"Free MEM: {gc.mem_free()}")
        x.append(label.Label(terminalio.FONT))
        y = displayio.Group()
        y.append(x)
        x = y
    except:
        print("FULL!")
        while True:
            try:
                import code
            except:
                print("TA")