#!/usr/bin/env python

import math
import time
import signal
import json
import paho.mqtt.client as mqtt

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

# anemometer
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# temperature / vane
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.IN)

def revs_to_speed(revs):
    mph = revs * 2.5
    return mph

def volt_to_temp(volt):
    temp = (54.35 * volt) - 15.44
    return temp

def volt_to_vane(volt):
    vane = (volt - 0.17) * 359 / 2.91
    return math.floor(vane)

class Counter:
    count = 0
    def read(self):
        revs = self.count
        self.count = 0
        return revs
    def increment(self):
        self.count += 1

anemometer = Counter()

class Accumulator:
    def __init__(self, many):
        self.many = many
        self.reset()

    def reset(self):
        self.speeds = []
        self.temps = []
        self.vanes = []

    def append(self, speed, temp, vane):
        self.speeds.append(speed)
        self.temps.append(temp)
        self.vanes.append(vane)
        if len(self.speeds) == self.many:
            avSpeed = sum(self.speeds) / len(self.speeds)
            avTemp = sum(self.temps) / len(self.temps)
            avVane = sum(self.vanes) / len(self.vanes)
            self.reset()
            self.store(avSpeed, avTemp, avVane)

    def store(self, mph, temp, vane):
        xmit_temp(time.time(), temp, mph, vane, None)

accumulator = Accumulator(1)

def alarm_handler(signum, frame):
    revs = anemometer.read()
    temp_volt = read_temp()
    vane_volt = read_vane()

    xmit_raw(time.time(), temp_volt, revs, vane_volt)

    mph = revs_to_speed(revs)
    temp = volt_to_temp(temp_volt)
    vane = volt_to_vane(vane_volt)
    accumulator.append(mph, temp, vane)

signal.signal(signal.SIGALRM, alarm_handler)
signal.setitimer(signal.ITIMER_REAL, 1, 1)

def my_callback(channel):
    anemometer.increment()

GPIO.add_event_detect(16, GPIO.FALLING, callback=my_callback, bouncetime=1)

def read_volt(channel):
    GPIO.output(24, True)
    GPIO.output(23, False)
    GPIO.output(19, True)

    word1 = [1, 1, channel, 1, 1]

    GPIO.output(24, False)
    anip = 0

    for x in range (0,5):
        GPIO.output(19, word1[x])
        GPIO.output(23, True)
        GPIO.output(23, False)

    for x in range (0,12):
        GPIO.output(23, True)
        bit = GPIO.input(21)
        GPIO.output(23, False)
        value=bit*2**(12-x-1)
        anip = anip + value

    GPIO.output(24, True)

    volt = anip*3.3/4096
    return volt

def read_temp():
    volt = read_volt(1)
    return volt

def read_vane():
    volt = read_volt(0)
    return volt

def xmit_raw(when, temp, speed, dir):
    client.publish("weather/raw", json.dumps({
        "time": when,
        "temp": temp,
        "speed": speed,
        "dir": dir
        }))

def xmit_temp(when, temp, speed, dir, rain):
    client.publish("weather/sample", json.dumps({
        "time": when,
        "temp": temp,
        "speed": speed,
        "dir": dir,
        "rain": rain
        }))

client = mqtt.Client()
client.connect("192.168.1.143", 1883, 60)

try:
    client.loop_forever()

except KeyboardInterrupt:
    GPIO.cleanup()
