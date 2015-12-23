#!/bin/sh

sqlite3 -batch $1 <<"EOF"
CREATE TABLE weather (time primary key, temp, speed, dir, rain);
EOF
