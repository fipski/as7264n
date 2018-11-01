#!/usr/bin/python3

import colsens

# test setup and config
colsens.setMux(0)
colsens.setup_col_sens()
temp = colsens.getTemp()
print("Temperature: " + str(temp))
colsens.setIntTime(0)
colsens.setGain(0b10)
colsens.setWtime(0)
colsens.setBank(1)
colsens.autoZero()




#calibrate to typical conditions
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

while 1:
    X, Y, Z, N = colsens.doMeasure(1)
    X, Y, Z = calibrate(X, Y, Z)
    X, Y, Z = normalize(X, Y, Z)
    x, y, Y = convertXYZtoxyY(X, Y, Z)

    print("x: " + str(x) )
    print("y: " + str(y) )
    print("Y: " + str(Y) )
    temp = colsens.getTemp()
    print("Temperature: " + str(temp))
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
