
start:
	mkdir -p log
	nohup ./sensors.py > log/sensors.log &
	nohup ./server.py > log/server.log &

mqtt:
	mkdir -p log
	nohup ./mqtt-sensors.py > log/mqtt-sensors.log &

stop:
	-pkill -f sensors.py
	-pkill -f server.py

db:
	./createdb.sh weather.db
