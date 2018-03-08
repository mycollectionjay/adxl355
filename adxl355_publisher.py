import mraa
import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime

_g_cst_ToMQTTTopicServerIP = "10.42.0.1"
_g_cst_ToMQTTTopicServerPort = 1883 #port
_g_cst_MQTTTopicName = "sensor/adxl" #TOPIC name
mqttc = mqtt.Client("python_pub")

if __name__ == '__main__':
	#connect with mqtt protocol
	mqttc.connect(_g_cst_ToMQTTTopicServerIP, _g_cst_ToMQTTTopicServerPort)
	mqttc.max_queued_messages_set(1000)

	bus = mraa.I2c(0)
	bus.address(0x1D)
	# ADXL355 address, 0x53(83)
	bus.writeReg(0x2C,0x81)
	#0x2C register:
	#bit 7:I2C speed
	#bit 6:interrupt polarity
	#bits [1:0]: range
	bus.writeReg(0x24,0x07)
	#0x24 register:
	#bit 2: active Z accl
	#bit 1: active Y accl
	#bit 0: active X accl
	bus.writeReg(0x2D,0x02)
	#0x2D register:
	#bit 2: DRDY on or off
	#bit 1: disable temperature measure
	#bit 0: STANDBY mode if 1

	time.sleep(0.5)
	counter=0

	while True:
		# ADXL345 address, 0x53(83)
		# Read data back from 0x32(50), 2 bytes
		# X-Axis LSB, X-Axis MSB
		st = bus.readReg(0x04)
		print "status: ",str(st)
		data0 = bus.readReg(0x08)
		data1 = bus.readReg(0x09)
		data2 = bus.readReg(0x0A)
		data0 *= 256*16
		data1 *= 16
		data2 &= 240
		data2 /= 16
		print str(data0+data1+data2)
		
		# Convert the data to 10-bits
		xAccl = data0+data1+data2
		if xAccl>=524288:
			xAccl=xAccl-1048576
		xAccl = (xAccl/524288.0)*2.048

		# ADXL345 address, 0x53(83)
		# Read data back from 0x34(52), 2 bytes
		# Y-Axis LSB, Y-Axis MSB
		data0 = bus.readReg(0x0B)
		data1 = bus.readReg(0x0C)
		data2 = bus.readReg(0x0D)
		data0 *= 256*16
		data1 *= 16
		data2 &= 240
		data2 /= 16
		print str(data0+data1+data2)
		
		# Convert the data to 10-bits
		yAccl = data0+data1+data2
		if yAccl>=524288:
			yAccl=yAccl-1048576
		yAccl = (yAccl/524288.0)*2.048

		# ADXL345 address, 0x53(83)
		# Read data back from 0x36(54), 2 bytes
		# Z-Axis LSB, Z-Axis MSB
		data0 = bus.readReg(0x0E)
		data1 = bus.readReg(0x0F)
		data2 = bus.readReg(0x10)
		data0 *= 256*16
		data1 *= 16
		data2 &= 240
		data2 /= 16
		print str(data0+data1+data2)
		
		# Convert the data to 10-bits
		zAccl = data0+data1+data2
		if zAccl>=524288:
			zAccl=zAccl-1048576
		zAccl = (zAccl/524288.0)*2.048

		# Output data to screen
		print "Acceleration in X-Axis : % 0.8f" %xAccl,
		print "Y-Axis : % 0.8fg\t" %yAccl,
		print "Z-Axis : % 0.8fg\t" %zAccl

		# Output data to screen
		#print "Acceleration in X-Axis : % 0.3f" %xAccl,
		#print "Y-Axis : % 0.3fg\t" %yAccl,
		#print "Z-Axis : % 0.3fg\t" %zAccl

		dt=datetime.now()
		strTime=str(dt.year)+'-'
		if dt.month/10<1:
			strTime=strTime+'0'
		strTime=strTime+str(dt.month)+'-'
		if dt.day/10<1:
			strTime=strTime+'0'
		strTime=strTime+str(dt.day)
		strTime=strTime+'T'
		if dt.hour/10<1:
			strTime+='0'
		strTime+=str(dt.hour)+':'
		if dt.minute/10<1:
			strTime+='0'
		strTime+=str(dt.minute)+':'
		if dt.second/10<1:
			strTime+='0'
		if len(str(dt.microsecond))<6:
            		for it in range(6-len(str(dt.microsecond))):
                    		strTime+='0'        
        		strTime+=str(dt.microsecond)
		
		
		if counter%1000==0:
			print "counter ",counter,":"
		if counter%10000==0:
			print strTime

		payload={'Date':time.strftime("%d/%m/%y"),'Time':strTime,'X':str(xAccl),'Y':str(yAccl),'Z':str(zAccl)}
		counter+=1
		mqttc.publish(_g_cst_MQTTTopicName, json.dumps(payload))
		#time.sleep(0.01)
