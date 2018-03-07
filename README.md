install pacakge
	Linkit 7688:
		pip install paho-mqtt
	
	Server:
		sudo pip install paho-mqtt
		sudo apt-get install mosquitto mosquitto-clients
		sudo pip install bokeh

python code
	adxl355_publisher.py: linkit 7688
	run_command.sh: run server
	adxl355_subscriber.py: run only mqtt subscriber
