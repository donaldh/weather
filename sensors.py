#!/usr/bin/env python

import math
import time
import signal
import sqlite3
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

print GPIO.RPI_INFO

# anemometer
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# temperature / vane
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.IN)

count = 0

def alarm_handler(signum, frame):
	mph = count * 2.5
	global count
	count = 0

	temp = read_temp()
	vane = read_vane()

	# print 'Measured %3.1f mph, dir %d, temperature %3.1fC' % (mph, vane, temp)
	write_temp(time.time(), temp, None, None, None)

signal.signal(signal.SIGALRM, alarm_handler)
signal.setitimer(signal.ITIMER_REAL, 1, 1)

def my_callback(channel):
	global count
	count += 1

GPIO.add_event_detect(16, GPIO.FALLING, callback=my_callback, bouncetime=10)

def read_volt(channel):
	GPIO.output(24, True)
	GPIO.output(23, False)
	GPIO.output(19, True)

	word1 = [1, 1, channel, 1, 1]

	GPIO.output(24, False)
	anip = 0

	for x in range (0,5):
		GPIO.output(19, word1[x])
		time.sleep(0.001)
		GPIO.output(23, True)
		time.sleep(0.001)
		GPIO.output(23, False)

	for x in range (0,12):
		GPIO.output(23, True)
		time.sleep(0.001)
		bit = GPIO.input(21)
		time.sleep(0.001)
		GPIO.output(23, False)
		value=bit*2**(12-x-1)
		anip = anip + value

	GPIO.output(24, True)

	volt = anip*3.3/4096
	return volt

def read_temp():
	volt = read_volt(1)
	temp = (55.5*volt) + 255.37 - 273.15
	return temp

def read_vane():
	volt = read_volt(0)
	vane = (volt - 0.17) * 359 / 2.91
	return math.floor(vane)

def write_temp(when, temp, speed, dir, rain):
	with sqlite3.connect('weather.db') as conn:
		cursor = conn.cursor()
		cursor.execute('INSERT into weather (time, temp, speed, dir, rain) values (cast(?*1000 as integer),round(?,1),?,?,?)', [when, temp, speed, dir, rain])

try:
    while 1:
	time.sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()
