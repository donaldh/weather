LAUNCHDIR=/Library/LaunchDaemons
PLIST=donaldh.weather.plist

WEBDIR=/usr/local/var/www/weather
WEBFILES=www/index.html

server:	## Run the server / mqtt collector
	mkdir -p log
	nohup ./server.py > log/server.log &

mqtt:	## Run the sensor / mqtt sender
	mkdir -p log
	nohup ./mqtt-sensors.py > log/mqtt-sensors.log &

stop-server:	## Stop the server
	-pkill -f server.py

stop-mqtt:	## Stop the sender
	-pkill -f mqtt-sensors.py

db:	## Create the sqlite db
	./createdb.sh weather.db

install:	## Install on mac host
	mkdir -p $(WEBDIR)
	cp $(WEBFILES) $(WEBDIR)
	sudo cp $(PLIST) $(LAUNCHDIR)
	sudo launchctl bootstrap system $(LAUNCHDIR)/$(PLIST)

shutdown:	## Disable server on mac host
	sudo launchctl bootout system/donaldh.weather

status:	## Report the server status on mac host
	sudo launchctl print system/donaldh.weather

help:	## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: help
.DEFAULT_GOAL := help
