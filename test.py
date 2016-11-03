#!/usr/bin/python3

import colsens
import colormath
from timeit import default_timer as timer

# test setup and config
colsens.setMux(0)
colsens.setup_col_sens()
# temp = colsens.getTemp()
# print("Temperature: " + str(temp))
colsens.setIntTime(255)
colsens.setGain(0b11)
colsens.setWtime(0)
colsens.setBank(0)
colsens.autoZero()
# setup sens 2
colsens.setMux(1)
colsens.setup_col_sens()
# temp = colsens.getTemp()
# print("Temperature: " + str(temp))
colsens.setIntTime(255)
colsens.setGain(0b11)
colsens.setWtime(0)
colsens.setBank(0)
colsens.autoZero()


# calibrate to typical conditions
# careful: typical values from the datasheet, no defined white point.

def calibrate(X, Y, Z):
    X=X/7.7
    Y=Y/8.6
    Z=Z/4.7
    return X, Y, Z

def normalize(X, Y, Z):
    maximum = max(X, Y, Z)
    X = X/maximum
    Y = Y/maximum
    Z = Z/maximum
    return X, Y, Z

def convertXYZtoxyY(X, Y, Z):
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)
    return x, y, Z

for i in range (0,2):
    print("X_" +str(i)+ ";", end = '')
    print("Y_" +str(i)+ ";", end = '')
    print("Z_" +str(i)+ ";", end = '')
    print("Temperature_" +str(i)+ ";", end = '')
    print("Time_" +str(i)+ ";", end = '')
print("")

while 1:
    for i in range (0,2):
        colsens.setMux(i)
        start = timer()
        X, Y, Z, N = colsens.doMeasure(1)
        # X, Y, Z = calibrate(X, Y, Z)
        # X, Y, Z = normalize(X, Y, Z)
        # x, y, Y = convertXYZtoxyY(X, Y, Z)
        end = timer()
        temp = colsens.getTemp()
        time = (end - start)
        end, start = 0,0
        print(str(X)+';' , end = '')
        print(str(Y)+';' , end = '')
        print(str(Z)+';' , end = '')
        print(str(temp)+';', end = '')
        print(str(time)+';', end = '')
    print("")

# from colormath.color_objects import XYZColor, HSLColor, AdobeRGBColor
# print("...import1...")
# from colormath.color_conversions import convert_color
# print("...import2...")
# xyz = XYZColor(x, y, z)
# rgb = convert_color(xyz, AdobeRGBColor)
#
# print("R: " + str(rgb.rgb_r))
# print("G: " + str(rgb.rgb_g))
# print("B: " + str(rgb.rgb_b))

# for x in range(0,100):
#     r = colsens.doMeasure(1)
#     r.printXYZ()
