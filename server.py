#!/usr/bin/env python

import json
import sqlite3
import BaseHTTPServer

def query_weather():
    with sqlite3.connect('weather.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT date, temp FROM weather WHERE date < ((select min(date) from weather) + (60 * 60 * 24))')
        data = cursor.fetchall()
        return data

class WeatherRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_head()
        print >>self.wfile, json.dumps(query_weather())

    def do_HEAD(self):
        self.send_head()

    def send_head(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

def run(server = BaseHTTPServer.HTTPServer,
        handler = WeatherRequestHandler):
    server_address = ('', 8000)
    httpd = server(server_address, handler)
    httpd.serve_forever()

run()
