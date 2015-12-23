#!/usr/bin/env python

import sqlite3
from flask import Flask, jsonify

app = Flask('Weather')
app.debug = True

def query_latest():
    with sqlite3.connect('weather.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT max(time) as time, ROUND(temp,1) from WEATHER")
        data = cursor.fetchall()
        return data[0]

def query_past_day():
    with sqlite3.connect('weather.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT max(time) as time, avg(temp) as temp FROM weather WHERE time > (strftime('%s','now') - 86400) group by cast(time / 300000 as integer)")
        data = cursor.fetchall()
        return data

@app.route('/day')
def weather():
    latest = query_latest()
    past_day = query_past_day()
    return jsonify(data=past_day, now=latest)

@app.after_request
def response_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
