#!/usr/bin/env python

import sqlite3
from flask import Flask, jsonify

app = Flask('Weather')
app.debug = True

def query_weather():
    with sqlite3.connect('weather.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT max(time) as time, avg(temp) as temp FROM weather WHERE time > (strftime('%s','now') - 86400) group by cast(time / 300 as integer)")
        data = cursor.fetchall()
        return data

@app.route('/')
def weather():
    return jsonify(data=query_weather())

@app.after_request
def response_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
