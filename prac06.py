#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os
import Adafruit_MCP3008

comboDir = [1,0,1]
comboLog = [2,1,2]
tic = 0

GPIO.setmode(GPIO.BCM)

# Buttons
sec_mode = 5
unsec_mode = 6

# Define callback functions
def callback1(channel):
	secure(channel)

def callback2(channel):
	unsecure(channel)

GPIO.setup(sec_mode, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(unsec_mode, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(sec_mode, GPIO.FALLING, callback = callback1, bouncetime = 500)
GPIO.add_event_detect(unsec_mode, GPIO.FALLING, callback = callback2, bouncetime = 500)


# Outputs
lock = 13
unlock = 19

GPIO.setup(unlock, GPIO.OUT)
GPIO.setup(lock, GPIO.OUT)
GPIO.output(unlock, GPIO.LOW)
GPIO.output(lock, GPIO.LOW)

CLK  = 11
MISO = 9
MOSI = 10
CS   = 8

# ADC Pins
GPIO.setup(MOSI, GPIO.OUT)
GPIO.setup(MISO, GPIO.IN)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)

mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

def ConvertVolts(data,places):
    volts = (data * 3.3) / float(1023)
    volts = round(volts,places)
    return volts

def reset():
    timer = time.time()

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
    print(list)

def checkDir(before, after):
	#tolerance for negligable changes in volts
	tolerance = 0.5    
	if (before - after > tolerance):
		return 0 	#Left turn
	elif (after - before > tolerance):
		return 1 	#Right turn
	else:
		return 2 	#No turn

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
		if combolog[i] != log[i]:
			GPIO.output(lock, GPIO.HIGH)
			time.sleep(2)
			GPIO.output(lock, GPIO.LOW)
			break
	GPIO.output(unlock, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(unlock, GPIO.LOW)


	
def main():
	log = [2, 9, 0]
	sort(log)
	GPIO.cleanup()
		
if __name__ == "__main__":
	main()
