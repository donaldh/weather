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

def query_past(conn, start):
    cursor = conn.cursor()
    cursor.execute("SELECT max(time) as time, avg(temp) as temp FROM weather WHERE time > ? group by cast(time / 300000 as integer)", [start])
    data = cursor.fetchall()
    return data

def query_date(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT strftime('%s', 'now') * 1000")
    data = cursor.fetchall()
    return data[0][0]

@app.route('/day')
def weather():
    with sqlite3.connect('weather.db') as conn:
        now = query_date(conn)
        start = now - 86400000
        latest = query_latest(conn)
        past_day = query_past(conn, start)
        return jsonify(data=past_day, now=latest, start=start, end=now)

@app.after_request
def response_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
