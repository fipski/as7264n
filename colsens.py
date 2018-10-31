#!/usr/bin/python3
import smbus
import time
import colormath


# I2C-Adresse des MCP23017
mux_addr = 0x70
sens_addr = 0x49

# Erzeugen einer I2C-Instanz und Oeffnen des Busses
bus = smbus.SMBus(2)
def setMux(i):
    bus.write_byte_data(mux_addr,0x00,0b00000001 << i) # select ch 1 on mux

def setup_col_sens():
    dev_id = bus.read_byte_data(sens_addr,0x10)
    print("Device id: " + str(dev_id))
    dev_ver = bus.read_byte_data(sens_addr,0x10)
    print("Device Version: " + str(dev_ver))

    # write device configuration
    bus.write_byte_data(sens_addr,0x70,0x8A) #Write dev_conf1
    bus.write_byte_data(sens_addr,0x71,0x02) #Write dev_conf2
    bus.write_byte_data(sens_addr,0xB0,0x02) #Write dev_conf3
    bus.write_byte_data(sens_addr,0x88,0x00) #Write dev_conf4
    bus.write_byte_data(sens_addr,0x9A,0x02) #Write dev_conf5

    # interrupt configuration
    intr_pin_config = 0x22
    intr_poll_clr = 0xF8
    intr_poll_en = 0xF9
    bus.write_byte_data(sens_addr,intr_pin_config,0x00) # disable interrupt pin
    bus.write_byte_data(sens_addr,intr_poll_clr,0x00) # configure for polling
    bus.write_byte_data(sens_addr,intr_pin_config,0x02) # configure for polling

    # turn off low power mode
    pwr_mode = 0x84
    bus.write_byte_data(sens_addr,pwr_mode,0x02) # bit 2 disables low pwr

# config, get temperature
tmp_config = 0xD3

def getTemp():
    bus.write_byte_data(sens_addr,tmp_config,0x24) # write 0x24 to get temp
    r = bus.read_byte_data(sens_addr,tmp_config)
    if r == 0x84:
        temp = bus.read_byte_data(sens_addr,0xD2) # read low byte
        temp  |= bus.read_byte_data(sens_addr,0xD1) << 2 # read hi byte
        temp = ((0.7604-((temp*2.048)/1024))/(2.046*0.001))-40 # convert to C
        bus.write_byte_data(sens_addr,tmp_config,0x00) # set to idle
        return temp
    else:
        return -1 # temp measurement not ready

def setIntTime(timeval): # set int time, should be 0-256
    # int_t = (256 - timeval) * 2.8
    bus.write_byte_data(sens_addr,0xD9,timeval)

def setGain(gain): # set gail level, 0b00 to 0b11
    bus.write_byte_data(sens_addr,0xB9,gain)

def setBank(bank): # set bank, 0 or 1
    bank = bank<<7
    bus.write_byte_data(sens_addr,0xDB,bank)

def setWtime(wtime): #set wait time, shoud be 0-256
    # int_t = (256 - timeval) * 2.8
    bus.write_byte_data(sens_addr,0xDA,wtime)

def autoZero():
    print("not done yet")
    # TODO

def startConversion():
    bus.write_byte_data(sens_addr,0xFA,0x01) # Write 0x01 to DATA_EN
    bus.write_byte_data(sens_addr,0xF8,0x01) # Write 0x01 to INTR_POLL_CLR
    bus.write_byte_data(sens_addr,0xFA,0x03) # Write 0x03 to Data_EN
    r = 0
    while r != 0x04:
        r = bus.read_byte_data(sens_addr,0xF8) # poll bit 2 of INTR_POLL_CLR, is hi when ready
    bus.write_byte_data(sens_addr,0xF8,0x04) # reset bit 2

def latchData():
    bus.write_byte_data(sens_addr,0xFA,0x83) # Write 0x83 to DATA_EN, latches data

def getChannel(addr):
    r = 0
    r = bus.read_byte_data(sens_addr,addr) # low byte
    r |= bus.read_byte_data(sens_addr, addr + 0x01) << 8 #hi byte
    return r

def getChannelN():
    return getChannel(0xDC)

def getChannelY():
    return getChannel(0xDE)

def getChannelZ():
    return getChannel(0xEC)

def getChannelX():
    return getChannel(0xEE)




# test stuff
setMux(0)
setup_col_sens()
temp = getTemp()
print("Temperature: " + str(temp))
setIntTime(0)
setGain(0b01)
setWtime(0)
setBank(1)
autoZero()
startConversion()
latchData()

N = getChannelN()
X = getChannelX()
Y = getChannelY()
Z = getChannelZ()

print("Channel N: " + str(N) )
print("Channel X: " + str(X) )
print("Channel Y: " + str(Y) )
print("Channel Z: " + str(Z) )

maximum = max(X, Y, Z)
x = X/maximum
y = Y/maximum
z = Z/maximum

print("Channel x: " + str(x) )
print("Channel y: " + str(y) )
print("Channel z: " + str(z) )

from colormath.color_objects import XYZColor, HSLColor, AdobeRGBColor
from colormath.color_conversions import convert_color
xyz = XYZColor(x, y, z)
rgb = convert_color(xyz, AdobeRGBColor)

print("R: " + str(rgb.rgb_r))
print("G: " + str(rgb.rgb_g))
print("B: " + str(rgb.rgb_b))
data_clr = 0xFA

led_drv = 0xEA
led_ind = 0x84



