#!/usr/bin/env python

import sqlite3
from flask import Flask, jsonify

app = Flask('Weather')
app.debug = True

def query_latest(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT max(time) as time, ROUND(temp,1) from WEATHER")
    data = cursor.fetchall()
    return data[0]

def query_past(conn, start, interval):
    cursor = conn.cursor()
    cursor.execute("SELECT max(time) as time, avg(temp) as temp FROM weather WHERE time > ? group by cast(time / ? as integer)", [start, interval])
    data = cursor.fetchall()
    return data

def query_date(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT strftime('%s', 'now') * 1000")
    data = cursor.fetchall()
    return data[0][0]

@app.route('/day')
def weather_day():
    return weather(86400000)

@app.route('/half')
def weather_half():
    return weather(43200000)

@app.route('/six')
def weather_six():
    return weather(21600000)

@app.route('/')
def weather_now():
    return weather(1000)

def weather(duration):
    with sqlite3.connect('weather.db') as conn:
        now = query_date(conn)
        start = now - duration
        latest = query_latest(conn)
        past_day = query_past(conn, start, duration / 150)
        return jsonify(data=past_day, now=latest, start=start, end=now)

@app.after_request
def response_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
