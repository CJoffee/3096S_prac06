#!/usr/bin/python

# Imports
import RPi.GPIO as GPIO
import time
import os
import Adafruit_MCP3008
# Combo arrays for combo unlock
comboDir = [0,1,0]
comboLog = [250.0,250.0,250.0]
tic = 0
delay = 50.0
tolerance = 0.01

# Log for 16 readings from potentiometer/Knob
log = []	# Start empty
dir = []
v_before = 0	# Starting position of the pot, will be read before loop
mode = 0	# 0 = secure, 1 = unsecure
dir_prev = 2	# Previous direction of turning
#n_log = 0;	# List iteration variable

# Set GPIO to BCM numbering
GPIO.setmode(GPIO.BCM)

# Buttons
sec_mode = 5
unsec_mode = 6

def callback_secure(channel):
	global mode
	global log
	global dir
	mode = 0
	log = []
	dir = []
	print("Secure mode enabled.")
	#GPIO.output(lock, GPIO.HIGH)

def callback_unsecure(channel):
	global mode
	global log
	global dir
	mode = 1
	log = []
	dir = []
	print("Insecure mode enabled.")

def secure():
	global log
	global comboLog
	global dir
	global comboDir
	#potVal = []
	#potVal.append(ConvertVolts(mcp.read_adc(7), 4))
	#potVal.pop(0)
	#bef = [0]*16
	true_flag = 1
	#if ((comboLog == log) and (comboDir == dir)):
	#if comboDir == dir:
	if (len(log)!=len(comboLog)):
		true_flag = 0
	for i in range(0, len(comboLog)):
		if abs(log[i]-comboLog[i])>delay:
			true_flag = 0
	if true_flag == 1:
		print("Unlocked!")
		GPIO.output(unlock, GPIO.HIGH)
		time.sleep(2)
		GPIO.output(unlock, GPIO.LOW)
	else:
		print("FAILED! System locked! Timings were:")
		print(log)
		GPIO.output(lock, GPIO.HIGH)
		time.sleep(2)
		GPIO.output(lock, GPIO.LOW)

def unsecure():
	global log
	global comboLog
	global delay
	sort(comboLog)
	sort(log)
	logs_equal = 1
	for i in range(len(comboLog)):
	#for i in range(len(comboDir)):
		#Check element-wise equality
		if abs(comboLog[i]-log[i])>delay:
		#if comboDir[i] != dir[i]:
			# If not equal, blink LOCK, then break loop
			GPIO.output(lock, GPIO.HIGH)
			print("FAILED! System locked! Timings were:")
			print(log)
			print("Timings should've been: ")
			print(comboLog)
			time.sleep(2)
			GPIO.output(lock, GPIO.LOW)
			logs_equal = 0
			break
	if logs_equal!=0:
		print("Unlocked!)
		GPIO.output(unlock, GPIO.HIGH)
		time.sleep(2)
		GPIO.output(unlock, GPIO.LOW)


# GPIO setup for buttons, set event detectors
GPIO.setup(sec_mode, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(unsec_mode, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(sec_mode, GPIO.FALLING, callback = callback_secure, bouncetime = 500)
GPIO.add_event_detect(unsec_mode, GPIO.FALLING, callback = callback_unsecure, bouncetime = 500)

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
	global timer
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
#    print(list)
    return list

# Check direction pot is turning
def checkDir(before, after):
	#tolerance for negligable changes in volts
	global tolerance
	if (before - after > tolerance):
		return 0 	#CW turn
	elif (after - before > tolerance):
		return 1 	#CCW turn
	else:
		return 2 	#No turn

	
def main():
	v_before = ConvertVolts(mcp.read_adc(7), 4)
	global delay
	dir_curr = 2
	twos = 0
	global dir_prev
	global tic

	print("Twiddle Lock system started! Secure mode enabled by default.")
	try:
		while True:
			#testlog = [0, 2, 1]
			global log
			global dir
			v_read = ConvertVolts(mcp.read_adc(7), 4)
			dir_curr = checkDir(v_before, v_read)
			if (dir_curr==2 and log):
				twos = twos+1
			if(dir_curr != 2 and dir_prev!=dir_curr and twos < 2000/delay):
				if(dir_prev != 2):
					log.append(tic*delay)
					dir.append(dir_prev)
					if(len(log)>16):
						log.pop(0)
						dir.pop(0)
					print("Timing (ms):", tic*delay,dir_prev) 
				# start timer again
				tic = 0
				twos = 0
				print("Current direction: ", dir_curr)

				#print("Previous direction: ", dir_prev)

				print("Timer started!")
			if(dir_curr == 2 and dir_prev!=dir_curr):
				# stop timer
				log.append(tic*delay)
				dir.append(dir_prev)

				print("Timing (ms): ", tic*delay)
				print("Direction: ", dir_prev)
			#print(dir_curr)

			if(mode == 0 and twos > float(2000.0/delay) and log):
					#secure mode
					print("Done! Secure check initiated.")
					print("Comparing to:")
					print(comboLog, comboDir)
					secure()
					break
			if(mode == 1 and twos > float(2000.0/delay) and log):
					#unsecure mode
					print("Done! Insecure check initiated.")
					print("Sorting and comparing to:")
					print(comboLog)
					unsecure()
					break
			v_before = v_read
			dir_prev = dir_curr
			tic = tic+1
#			print("TICK!")
			time.sleep(float(delay/1000))
		GPIO.cleanup()

	except KeyboardInterrupt:
		print(log)
		print(dir)
		GPIO.cleanup()


if __name__ == "__main__":
	main()
