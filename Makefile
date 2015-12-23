
start:
	nohup ./sensors.py > sensors.log &
	nohup ./server.py > server.log &

stop:
	pkill -f sensors.py
	pkill -f server.py
