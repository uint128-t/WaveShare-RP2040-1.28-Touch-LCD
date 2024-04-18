import displayio,busio,gc9a01,board,cst816

displayio.release_displays()
print("Display setup")

spi = busio.SPI(clock=board.LCD_CLK, MOSI=board.LCD_DIN)
display_bus = displayio.FourWire(spi, command=board.LCD_DC, chip_select=board.LCD_CS, reset=board.LCD_RST)
display = gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=board.LCD_BL)

i2c = busio.I2C(board.IMU_SCL,board.IMU_SDA)
# What? IMU stands for INERTIAL MEASUREMENT UNIT but we're connecting a TOUCHSCREEN? (cant connect IMU?)
touch = cst816.CST816(i2c)