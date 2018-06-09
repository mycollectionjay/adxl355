import sys
import mraa
import time
import json
import socket
from datetime import datetime


if __name__ == '__main__':
	#connect with mqtt protocol

	bus = mraa.I2c(0)
	bus.address(0x1D)
	# ADXL355 address, 0x53(83)
	bus.writeReg(0x2C,0x01)
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
	last_t = time.time()
	counter=0

	dataList=[]
	data = [[ [] for j in range(3)] for i in range(3)] 
	HOST = '10.42.0.1'
	PORT = 50007
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	#x y z
	while True:
		now_t = time.time()
		if now_t - last_t >= 0.005:
			last_t = now_t
			# ADXL345 address, 0x53(83)
			# Read data back from 0x32(50), 2 bytes
			# X-Axis LSB, X-Axis MSB
			st = bus.readReg(0x04)
			#print "status: ",str(st)
			data[0][0] = int(bus.readReg(0x08))
			data[0][1] = int(bus.readReg(0x09))
			data[0][2] = int(bus.readReg(0x0A))


			# ADXL345 address, 0x53(83)
			# Read data back from 0x34(52), 2 bytes
			# Y-Axis LSB, Y-Axis MSB
			data[1][0] = int(bus.readReg(0x0B))
			data[1][1] = int(bus.readReg(0x0C))
			data[1][2] = int(bus.readReg(0x0D))

			# Z-Axis LSB, Z-Axis MSB
			data[2][0] = int(bus.readReg(0x0E))
			data[2][1] = int(bus.readReg(0x0F))
			data[2][2] = int(bus.readReg(0x10))

		

			if counter==1000:		
				init_t = time.time()
			if counter>=6000:
				print "Time Spent for 1000 datas: ", time.time()-init_t
				s.send('*')
				break
			#payload={'X':str(xAccl),'Y':str(yAccl),'Z':str(zAccl)}
			counter+=1
			if counter>1000:
				s.send(str(format(last_t, '.6f')) + '&' + repr(data) +"#")
				#dataList.append(str(format(last_t, '.4f')) + '\t' + str(data))
		#time.sleep(0.01)
	s.close() 
	# fwrite = open('Output','w')
	# for s in dataList:
	# 	fwrite.write(s+'\n')
