#!/usr/bin/python3

# quick script to read values.
# TODO
# class for sensor
# flexible i2c bus
#
# needs smbus


import smbus
import time

mux_addr = 0x70      # i2c Adresse des MCP23017
sens_addr = 0x49     # i2c Adresse des as7264n
bus = smbus.SMBus(2) # i2c bus 2

class XYZN(object):
    def __init__(self, X, Y, Z, N):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.N = N
    def __str__(self):
        r =  "X: " + str(self.X)
        r += "Y: " + str(self.Y)
        r += "Z: " + str(self.Z)
        r += "N: " + str(self.N)
        return r

def setMux(i):
    if 0 <= i <= 7:
        bus.write_byte_data(mux_addr,0x00,0b00000001 << i) # select ch 1 on mux
    else:
        raise ValueError('channel must be 0...7')

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
def getTemp():
    tmp_config = 0xD3 # TMP_CONFIG Address
    bus.write_byte_data(sens_addr,tmp_config,0x24) # write 0x24 to get temp
    r = 0
    while r != 0x84: # check if temperature measurement is ready
        r = bus.read_byte_data(sens_addr,tmp_config)
    temp = bus.read_byte_data(sens_addr,0xD2) # read low byte
    temp  |= bus.read_byte_data(sens_addr,0xD1) << 2 # read hi byte
    temp = ((0.7604-((temp*2.048)/1024))/(2.046*0.001))-40 # convert to C
    bus.write_byte_data(sens_addr,tmp_config,0x00) # set to idle
    return temp

def setIntTime(timeval): # set int time, should be 0-255
    if 0 <= timeval <= 255:
    # t = (256 - timeval) * 2.8
        try:
            bus.write_byte_data(sens_addr,0xD9,timeval)
        except IOError, err:
            print err
    else:
        raise ValueError('time must be 0...255')


def setGain(gain): # set gail level, 0b00 to 0b11
    if 0 <= gain <= 3:
        bus.write_byte_data(sens_addr,0xB9,gain)
    else:
        raise ValueError('gain must be 0...3')

def setBank(bank): # set bank, 0 or 1
    if 0 <= bank <= 1:
        bank = bank<<7
        bus.write_byte_data(sens_addr,0xDB,bank)
    else:
        raise ValueError('bank must be 0...1')

def setWtime(wtime): #set wait time, shoud be 0-255
    # t = (256 - timeval) * 2.8
    if 0 <= wtime <= 255:
        bus.write_byte_data(sens_addr,0xDA,wtime)
    else:
        raise ValueError('wtime must be 0...255')

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
    r |= bus.read_byte_data(sens_addr, addr + 0x01) << 8 # hi byte
    return r

def getChannelN():
    return getChannel(0xDC)

def getChannelY():
    return getChannel(0xDE)

def getChannelZ():
    return getChannel(0xEC)

def getChannelX():
    return getChannel(0xEE)

def doMeasure(bank):
    setBank(bank)
    # autoZero()
    startConversion()
    latchData()
    N = getChannelN()
    X = getChannelX()
    Y = getChannelY()
    Z = getChannelZ()
    return X, Y, Z, N
