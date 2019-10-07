import serial
import time
import sys
sys.path.append('..')
import Dpm8600
# Controls a supply, ramping from 0V to 12V.

SUPPLY1 = "USB0"

p1 = Dpm8600.Dpm8600(SUPPLY1)

p1.v(0)
p1.a(500)

p1.on()

for volts in range(121):
	p1.v(str(volts) + "0")
p1.off()
