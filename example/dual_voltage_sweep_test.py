import serial
import time
import sys
sys.path.append('..')
import Dpm8600
# Controls two power supplies, ramping one from 0V to 12V and the other from 12V to 0V.

SUPPLY1 = "USB0"
SUPPLY2 = "USB1"

p1 = Dpm8600.Dpm8600(SUPPLY1)
p2 = Dpm8600.Dpm8600(SUPPLY2)

#time.sleep(5)
p1.v(0)
p2.v(0)

p1.on()
p2.on()

for volts in range(121):
	p1.v(str(volts) + "0")
	p2.v(str(121 - volts) + "0")
p1.off()
p2.off()
