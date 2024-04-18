# This is an implementation of the Waveshare 1.28" LCD RP2040 Board
# https://www.waveshare.com/wiki/1.28inch_LCD_RP2040_Board
# It uses the CircuitPython libraries and the GC9A01 display driver
# https://circuitpython.readthedocs.io/projects/gc9a01/en/latest/
# I had to implement my own battery and IMU classes because the
# existing ones didn't work with CircuitPython.  
# @author: Jesse R. Castro
# @TODO: Add menu class
# @TODO: Record accelerometer data to a file for calibration

import random
import time
from math import floor

import board
import busio
import displayio
import gc9a01
import terminalio
import analogio
import digitalio
import vectorio

from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# A generic class to describe battery status, should 
# work with any battery that has a voltage between 3.2V
# and 4.3V
class Battery(object):
    # Initialize the battery
    # returns: nothing
    def __init__(self, pin=board.BAT_ADC):
        self._pin = analogio.AnalogIn(pin)
        self._max_voltage = 4.14
        self._min_voltage = 3.4
        self._max_diff = self._max_voltage - self._min_voltage
        self._diff = 0.0
        self._voltage = 0.0
        self._percent = 0.0
        self._charging = False
        self._discharging = False
        self._full = False
        self._empty = False
        self._update()

    # Update the battery status
    # returns: nothing
    def _update(self):
        # Read the battery voltage
        self._voltage = self._pin.value * 3.3 / 65535 * 2
        self._diff = self._max_voltage - self._voltage
        # Convert the voltage to a percentage
        if self._voltage > self._max_voltage:
            self._percent = 100.0
        elif self._voltage < self._min_voltage:
            self._percent = 0.0
        else:
            self._percent = (self._diff / self._max_diff) * 100.0 
        # Determine the charging status
        if self._voltage > 4.14:
            self._charging = True
            self._discharging = False
            self._full = True
            self._empty = False
        elif self._voltage < 3.4:
            self._charging = False
            self._discharging = False
            self._full = False
            self._empty = True
        else:
            self._charging = False
            self._discharging = True
            self._full = False
            self._empty = False

    # Get the battery voltage
    # returns: the battery voltage
    @property
    def voltage(self):
        self._update()
        return self._voltage

    # Get the battery percentage
    # returns: the battery percentage
    @property
    def percent(self):
        self._update()
        return self._percent

    # Get the charging status
    # returns: True if the battery is charging, False otherwise
    @property
    def charging(self):
        self._update()
        return self._charging

    # Get the discharging status
    # returns: True if the battery is discharging, False otherwise
    @property
    def discharging(self):
        self._update()
        return self._discharging

# A class to interface with a Microchip QMI8658 6-axis IMU
# https://www.microchip.com/wwwproducts/en/QMI8658
# Working code already exists in micropython, this is an 
# adaptation of that code for use with CircuitPython (see
# micro.py for the original code)
class QMI8658_Accelerometer(object):
    # Initialize the hardware
    # address: the I2C address of the device
    # returns: nothing
    def __init__(self,address=0X6B, scl=board.GP7, sda=board.GP6):
        self._address = address
        self._bus = busio.I2C(scl,sda)
        if self.who_am_i():
            self.rev = self.read_revision()
        else:
            raise Exception("QMI8658 not found")
        self.config_apply()
    
    # Read a byte from the specified register
    # register: the register to read from
    # returns: the byte read
    def _read_byte(self,register):
        return self._read_block(register,1)[0]

    # Read a block of bytes from the specified register
    # register: the register to begin the read from
    # length: the number of bytes to read
    # returns: a list of bytes read
    def _read_block(self, register, length=1):
        while not self._bus.try_lock():
            pass
        try:
            rx = bytearray(length)
            self._bus.writeto(self._address, bytes([register]))
            self._bus.readfrom_into(self._address, rx)
        finally:
            self._bus.unlock()    
        return rx
    
    # Read a 16-bit unsigned integer from the specified register
    # register: the register to begin the read from
    # returns: the 16-bit unsigned integer read
    def _read_u16(self,register):
        return (self._read_byte(register) << 8) + self._read_byte(register+1)

    # Write a byte to the specified register
    # register: the register to write to
    # value: the byte to write
    # returns: nothing    
    def _write_byte(self,register,value):
        while not self._bus.try_lock():
            pass
        try:
            self._bus.writeto(self._address, bytes([register, value]))
            #self._bus.writeto(self._address, bytes([value]))
        finally:
            self._bus.unlock()

    # Make sure this device is what it thinks it is
    # returns: True if the device is what it thinks it is, False otherwise  
    def who_am_i(self):
        bRet=False
        rec = self._read_byte(0x00)
        if (0x05) == rec:
            bRet = True   
        return bRet

    # Read the revision of the device
    # returns: the revision of the device
    def read_revision(self):
        return self._read_byte(0x01)

    # Apply the configuration to the device by writing to 
    # the appropriate registers.  See device datasheet for
    # details on the configuration.
    # returns: nothing    
    def config_apply(self):
        # REG CTRL1
        self._write_byte(0x02,0x60)
        # REG CTRL2 : QMI8658AccRange_8g  and QMI8658AccOdr_1000Hz
        self._write_byte(0x03,0x23)
        # REG CTRL3 : QMI8658GyrRange_512dps and QMI8658GyrOdr_1000Hz
        self._write_byte(0x04,0x53)
        # REG CTRL4 : No
        self._write_byte(0x05,0x00)
        # REG CTRL5 : Enable Gyroscope And Accelerometer Low-Pass Filter 
        self._write_byte(0x06,0x11)
        # REG CTRL6 : Disables Motion on Demand.
        self._write_byte(0x07,0x00)
        # REG CTRL7 : Enable Gyroscope And Accelerometer
        self._write_byte(0x08,0x03)

    # Read the raw accelerometer and gyroscope data from the device
    # returns: a list of 6 integers, the first 3 are the accelerometer
    #          data, the last 3 are the gyroscope data
    def read_raw_xyz(self):
        xyz=[0,0,0,0,0,0]
        raw_timestamp = self._read_block(0x30,3)
        raw_acc_xyz=self._read_block(0x35,6)
        raw_gyro_xyz=self._read_block(0x3b,6)
        raw_xyz=self._read_block(0x35,12)
        timestamp = (raw_timestamp[2]<<16)|(raw_timestamp[1]<<8)|(raw_timestamp[0])
        for i in range(6):
            # xyz[i]=(raw_acc_xyz[(i*2)+1]<<8)|(raw_acc_xyz[i*2])
            # xyz[i+3]=(raw_gyro_xyz[((i+3)*2)+1]<<8)|(raw_gyro_xyz[(i+3)*2])
            xyz[i] = (raw_xyz[(i*2)+1]<<8)|(raw_xyz[i*2])
            if xyz[i] >= 32767:
                xyz[i] = xyz[i]-65535
        return xyz

    # Read the accelerometer and gyroscope data from the device and return
    # in human-readable format.
    # returns: a list of 6 floats, the first 3 are the accelerometer
    #         data, the last 3 are the gyroscope data    
    def read_xyz(self):
        xyz=[0,0,0,0,0,0]
        raw_xyz=self.read_raw_xyz()  
        #QMI8658AccRange_8g
        acc_lsb_div=(1<<12)
        #QMI8658GyrRange_512dps
        gyro_lsb_div = 64
        for i in range(3):
            xyz[i]=raw_xyz[i]/acc_lsb_div#(acc_lsb_div/1000.0)
            xyz[i+3]=raw_xyz[i+3]*1.0/gyro_lsb_div
        return xyz
