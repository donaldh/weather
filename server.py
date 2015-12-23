#!/usr/bin/env python

import json
import sqlite3
import BaseHTTPServer

def query_weather():
    with sqlite3.connect('weather.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT max(time) as time, avg(temp) as temp FROM weather WHERE time > (strftime('%s','now') - 86400) group by cast(time / 60 as integer)")
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
