'''
Control a DPM-8600 series power supply
Compatible with the simple serial protocol
USB Serial cable wiring:
	Red ---- (do not connect)
	Wht ------ A
	Grn ------ B
	Blk ---- GND
'''

import serial
import time
import re

QUIET  = -1
ERROR  =  0
WARN   =  1
INFO   =  2
DEBUG  =  3

class Dpm8600:
	verbosity     = QUIET
	cmd_setv      = "w10="      # Set V
	cmd_seta      = "w11="      # Set A
	cmd_setva     = "w20="      # Set both V/A
	cmd_on        = "w12=1"     # Set pwr on
	cmd_off       = "w12=0"     # Set pwr off
	cmd_status    = "r12=0"     # Read pwr status
	cmd_temp      = "r33=0"     # Read temperature
	cmd_getvcap   = "r10=0"     # Read both V cap
	cmd_getacap   = "r11=0"     # Read both A cap
	cmd_getvval   = "r30=0"     # Read V value
	cmd_getaval   = "r31=0"     # Read A value
	cmd_getva     = "r20=0"     # Read both V/A
	cmd_getcap    = "r32=0"     # Read CC or CV status
	ser = False

	def __init__(self, port, baud = 9600, verbosity = QUIET):
		self.debug("DPM Loading")
		self.verbosity = verbosity
		self.ser = serial.Serial("/dev/tty" + port, baud, timeout = 0.5)

	def __del__(self):
		self.debug("DPM Unoading")
		if self.ser != False:
			self.ser.close()

	def do(self, cmd):
		cmd = ":01" + cmd + ","
		self.debug(cmd, DEBUG)
		bytes_written = self.ser.write((cmd + "\r\n").encode())

		# capture the ACK instead of using a timer
		buf = ""
		while True:
			buf = buf + self.ser.read(1).decode()
			if len(buf) > 1 and buf[-4:] == "ok\r\n":
				self.debug("ACK", DEBUG)
				return

	def get(self, cmd):
		cmd = ":01" + cmd + ","
		self.debug(cmd, DEBUG)
		bytes_written = self.ser.write((cmd + "\r\n").encode())
		buf = ""
		while True:
			buf = buf + self.ser.read(1).decode()
			if len(buf) > 1 and buf[-4:] == "ok\r\n":
				buf = "" # Ignore command acks
			if len(buf) > 1 and buf[-2:] == "\r\n":
				return re.search("=(.*)\.", buf[0:-2]).group(1)

	def v(self, volts):
		volts = str(volts)
		self.debug("Setting max V: " + volts)
		cmd = self.cmd_setv + volts.zfill(4)
		self.do(cmd)

	def a(self, amps):
		amps = str(amps)
		self.debug("Setting max A: " + amps)
		cmd = self.cmd_seta + amps.zfill(4)
		self.do(cmd)

	def va(self, volts, amps):
		volts = str(volts)
		amps = str(amps)
		self.debug("Setting max VA: " + volts + "," + amps)
		cmd = self.cmd_setva + volts.zfill(4) + "," + amps.zfill(4)
		self.do(cmd)

	def on(self):
		self.debug("Output on")
		self.do(self.cmd_on)

	def off(self):
		self.debug("Output off")
		self.do(self.cmd_off)

	def temp(self):
		self.debug("Getting temperature")
		out = self.get(self.cmd_temp)
		self.debug(out)

	def pwrstatus(self):
		self.debug("Getting power status")
		out = self.get(self.cmd_status)
		self.debug(out)

	def getvcap(self):
		self.debug("Reading max V")
		out = self.get(self.cmd_getvcap)
		self.debug(out)

	def getacap(self):
		self.debug("Reading max A")
		out = self.get(self.cmd_getacap)
		self.debug(out)

	def getvval(self):
		self.debug("Reading actual V")
		out = self.get(self.cmd_getvval)
		self.debug(out)

	def getaval(self):
		self.debug("Reading actual A")
		out = self.get(self.cmd_getaval)
		self.debug(out)

	def getva(self):
		self.debug("Reading VA")
		out = self.get(self.cmd_getva)
		self.debug(out)

	def getcap(self):
		self.debug("Reading Limit Type")
		out = ("cc" if self.get(self.cmd_getcap) == "1" else 'cv')
		self.debug(out)

	def debug(self, msg, lvl = INFO):
		if self.verbosity >= lvl:
			print(msg) 
