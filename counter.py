#!/usr/bin/env python

import time
import signal
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

print GPIO.RPI_INFO

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

count = 0

def alarm_handler(signum, frame):
	print "Counted", count * 2.5, 'mph'
	global count
	count = 0

signal.signal(signal.SIGALRM, alarm_handler)
signal.setitimer(signal.ITIMER_REAL, 1, 1)

def my_callback(channel):
	global count
	count += 1

GPIO.add_event_detect(16, GPIO.FALLING, callback=my_callback, bouncetime=10)

try:
    while 1:
	time.sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()
