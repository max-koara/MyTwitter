# coding: utf-8
#
# FaBo Brick Sample
#
# brick_i2c_temp
#

import smbus
import time
import FaBoTemperature_ADT7410

adt7410 = FaBoTemperature_ADT7410.ADT7410()

while True:
	data = adt7410.read()
	print data
