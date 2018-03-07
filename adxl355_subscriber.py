import paho.mqtt.client as mqtt
from datetime import datetime
import time

count=0
cur=time.time()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("sensor/adxl")
 
def on_message(client, userdata, msg):
	#print(msg.topic+" "+str(msg.payload))
	dt=datetime.now()
	global count
	global cur
	if time.time()-cur>1:
		print "Data Received:",count
		count=0
		cur=time.time()
	count+=1
 
client = mqtt.Client()
#needed so that connection can be established
user = "ice"
password = "dscrtpwr"
client.username_pw_set(user, password)
client.on_connect = on_connect
client.on_message = on_message
try:    
    client.connect("192.168.11.17", 1883, 10)  
    client.loop_forever()  
except KeyboardInterrupt:  
    client.disconnect()
