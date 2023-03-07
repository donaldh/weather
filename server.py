#!/usr/bin/env python

import math
import json
import time
import sqlite3
import paho.mqtt.client as mqtt
from flask import Flask, jsonify

class Accumulator:
    def __init__(self, many):
        self.many = many
        self.reset()

    def reset(self):
        self.speeds = []
        self.temps = []
        self.vanes = []

    def average_bearings(self):
        x = y = 0
        for a in self.vanes:
            x += math.cos(math.radians(a))
            y += math.sin(math.radians(a))

        ave = math.atan2(y, x)
        return (int(math.degrees(ave)) + 360) % 360

    def append(self, speed, temp, vane):
        self.speeds.append(speed)
        self.temps.append(temp)
        self.vanes.append(vane)
        if len(self.speeds) == 10:
            avSpeed = sum(self.speeds) / len(self.speeds)
            avTemp = sum(self.temps) / len(self.temps)
            avVane = self.average_bearings()
            self.reset()
            self.store(avSpeed, avTemp, avVane)

    def store(self, mph, temp, vane):
        # print 'Measured %3.1f mph, dir %d, temperature %3.1fC' % (mph, vane, temp)
        write_temp(time.time(), temp, mph, vane, None)

def write_temp(when, temp, speed, dir, rain):
    with sqlite3.connect('weather.db') as conn:
        cursor = conn.cursor()
        # print(f"{when} {temp} {speed} {dir}")
        try:
            cursor.execute('INSERT into weather (time, temp, speed, dir, rain) values (cast(? as integer),round(?,1),?,?,?)',
                           [when, temp, speed, dir, rain])
        except:
            pass

accumulator = Accumulator(10)

app = Flask('Weather')
app.debug = True

def query_latest(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT max(time) * 1000 as time, ROUND(temp,1), ROUND(speed,1), ROUND(dir,0) from WEATHER")
    data = cursor.fetchall()
    return data[0]

def query_past(conn, start, interval):
    cursor = conn.cursor()
    cursor.execute("SELECT max(time) * 1000 as time, avg(temp) as temp, avg(speed) as speed, avg(dir) as dir FROM weather WHERE time > ? group by cast(time / ? as integer)", [start, interval])
    data = cursor.fetchall()
    return data

def query_date(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT strftime('%s', 'now')")
    data = cursor.fetchall()
    return int(data[0][0])

@app.route('/seven-days')
def weather_seven_days():
    return weather(86400 * 7)

@app.route('/three-days')
def weather_three_days():
    return weather(86400 * 3)

@app.route('/day')
def weather_day():
    return weather(86400)

@app.route('/half')
def weather_half():
    return weather(43200)

@app.route('/six')
def weather_six():
    return weather(21600)

@app.route('/')
def weather_now():
    return weather(1000)

def weather(duration):
    with sqlite3.connect('weather.db') as conn:
        now = query_date(conn)
        start = now - duration
        latest = query_latest(conn)
        data = query_past(conn, start, duration / 143)
        return jsonify(data=data, samples=len(data), now=latest, start=start * 1000, end=now * 1000)

@app.after_request
def response_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['X-Clacks-Overhead'] = 'GNU Terry Pratchett'
    return response

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("weather/sample")

def on_message(client, userdata, msg):
    sample = json.loads(msg.payload)
    accumulator.append(sample['speed'], sample['temp'], sample['dir'])

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_start()

    app.run(host='0.0.0.0', port=8000, threaded=True)
