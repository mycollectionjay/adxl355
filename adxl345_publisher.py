import mraa
import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime

_g_cst_ToMQTTTopicServerIP = "10.42.0.83"
_g_cst_ToMQTTTopicServerPort = 1883 #port
_g_cst_MQTTTopicName = "sensor/adxl" #TOPIC name
mqttc = mqtt.Client("python_pub")

if __name__ == '__main__':
	#connect with mqtt protocol
	mqttc.connect(_g_cst_ToMQTTTopicServerIP, _g_cst_ToMQTTTopicServerPort)

	bus = mraa.I2c(0)
	bus.address(0x53)
	# ADXL345 address, 0x53(83)
	# Select bandwidth rate register, 0x2C(44)
	#		0x0A(10)	Normal mode, Output data rate = 100 Hz
	bus.writeReg(0x2C,0x0A)
	# ADXL345 address, 0x53(83)
	# Select power control register, 0x2D(45)
	#		0x08(08)	Auto Sleep disable
	bus.writeReg(0x2D,0x08)
	# ADXL345 address, 0x53(83)
	# Select data format register, 0x31(49)
	#		0x08(08)	Self test disabled, 4-wire interface
	#					Full resolution, Range = +/-2g
	bus.writeReg(0x31,0x08)

	time.sleep(0.5)
	counter=0

	while 1:
		# ADXL345 address, 0x53(83)
		# Read data back from 0x32(50), 2 bytes
		# X-Axis LSB, X-Axis MSB
		data0 = bus.readReg(0x32)
		data1 = bus.readReg(0x33)
		#print str(data0+data1*256)
		
		# Convert the data to 10-bits
		xAccl = data0+data1*256
		if xAccl>=32768:
			xAccl=xAccl%32768
			xAccl=32768-xAccl
			xAccl*=-1
		xAccl=xAccl*0.004


		# ADXL345 address, 0x53(83)
		# Read data back from 0x34(52), 2 bytes
		# Y-Axis LSB, Y-Axis MSB
		data0 = bus.readReg(0x34)
		data1 = bus.readReg(0x35)
		#print str(data0+data1*256)

		# Convert the data to 10-bits
		yAccl = data0+data1*256
		if yAccl>=32768:
			yAccl=yAccl%32768
			yAccl=32768-yAccl
			yAccl*=-1
		yAccl=yAccl*0.004

		# ADXL345 address, 0x53(83)
		# Read data back from 0x36(54), 2 bytes
		# Z-Axis LSB, Z-Axis MSB
		data0 = bus.readReg(0x36)
		data1 = bus.readReg(0x37)
		#print str(data0+data1*256)

		# Convert the data to 10-bits
		zAccl = data0+data1*256
		if zAccl>=32768:
			zAccl=zAccl%32768
			zAccl=32768-zAccl
			zAccl*=-1
		zAccl=zAccl*0.004

		# Output data to screen
		#print "Acceleration in X-Axis : % 0.3f" %xAccl,
		#print "Y-Axis : % 0.3fg\t" %yAccl,
		#print "Z-Axis : % 0.3fg\t" %zAccl

		dt=datetime.now()
		strTime=str(dt.hour)+':'+str(dt.minute)+':'+str(dt.second)+':'+str(dt.microsecond)

		if counter%1000==0:
			print "counter ",counter,":"
		if counter%10000==0:
			print strTime

		payload={'Date':time.strftime("%d/%m/%y"),'Time':strTime,'X':str(xAccl),'Y':str(yAccl),'Z':str(zAccl)}
		counter+=1
		mqttc.publish(_g_cst_MQTTTopicName, json.dumps(payload))
		#time.sleep(0.01)
