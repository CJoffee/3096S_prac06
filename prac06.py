#!/usr/bin/python

# Imports
import RPi.GPIO as GPIO
import time
import os
import Adafruit_MCP3008

# Combo arrays for combo unlock
comboDir = [1,0,1]
comboLog = [2,1,2]
tic = 0

# Log for 16 readings from potentiometer/Knob
log = [None]*16	# Start empty
dir = [None]*16
n_log = 0;	# List iteration variable

# Set GPIO to BCM numbering
GPIO.setmode(GPIO.BCM)

# Buttons
sec_mode = 5
unsec_mode = 6

def secure(channel):
	potVal = [0]*16
	potVal.append(ConvertVolts(mcp.read_adc(7), 4))
	potVal.pop(0)
	bef = [0]*16

	if ((comboLog == log) and (comboDir == dir)):
		GPIO.output(unlock, GPIO.HIGH)
		time.sleep(2)
		GPIO.output(unlock, GPIO.LOW)
	else:
		GPIO.output(lock, GPIO.HIGH)
		time.sleep(2)
		GPIO.output(lock, GPIO.LOW)

def unsecure(channel):
	sort(combolog)
	sort(log)
	for i in range(len(combolog)):
		# Check element-wise equality
		if combolog[i] != log[i]:
			# If not equal, blink LOCK, then break loop
			GPIO.output(lock, GPIO.HIGH)
			time.sleep(2)
			GPIO.output(lock, GPIO.LOW)
			break
	GPIO.output(unlock, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(unlock, GPIO.LOW)


# GPIO setup for buttons, set event detectors
GPIO.setup(sec_mode, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(unsec_mode, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(sec_mode, GPIO.FALLING, callback = secure, bouncetime = 500)
GPIO.add_event_detect(unsec_mode, GPIO.FALLING, callback = unsecure, bouncetime = 500)

# Outputs
lock = 13
unlock = 19

# LED displays for locked/unlocked
GPIO.setup(unlock, GPIO.OUT)
GPIO.setup(lock, GPIO.OUT)
GPIO.output(unlock, GPIO.LOW)
GPIO.output(lock, GPIO.LOW)

# MCP3008 pin numbers
CLK  = 11	
MISO = 9	# Read voltage here
MOSI = 10	
CS   = 8

# ADC Pins setup
GPIO.setup(MOSI, GPIO.OUT)
GPIO.setup(MISO, GPIO.IN)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)

# Initialise ADC
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Convert _data_ to volts, to _places_ decimal places
def ConvertVolts(data,places):
    volts = (data * 3.3) / float(1023)
    volts = round(volts,places)
    return volts

# Reset timer
def reset():
    timer = time.time()

# Python sort, select sort
def sort(list):
    for index in range(1,len(list)):
        value = list[index]
        i = index-1
        while i>=0:
            if value < list[i]:
                list[i+1] = list[i]
                list[i] = value
                i -= 1
            else:
                break
    return list

# Check direction pot is turning
def checkDir(before, after):
	#tolerance for negligable changes in volts
	tolerance = 0.5    
	if (before - after > tolerance):
		return 0 	#Left turn
	elif (after - before > tolerance):
		return 1 	#Right turn
	else:
		return 2 	#No turn

	
def main():
	try:
		while True:
			testlog = [0 2 1]
			sort(testlog)
			//print(testlog)

	except KeyboardInterrupt:
		GPIO.cleanup()
		
		
if __name__ == "__main__":
	main()
