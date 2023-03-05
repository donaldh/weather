
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

help:	## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: help
.DEFAULT_GOAL := help
