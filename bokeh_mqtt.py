# myplot.py
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
import random
import paho.mqtt.client as mqtt
import json
import threading
import time

buffer_x=0
buffer_y=0
buffer_z=0
count=0
cur=time.time()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("sensor/adxl")
 
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    decode=json.loads(msg.payload.decode("utf=8"))
    thread.x=float(decode["X"])
    thread.y=float(decode["Y"])
    thread.z=float(decode["Z"])
    thread.lock=False
 
client = mqtt.Client()
#needed so that connection can be established
user = "ice"
password = "dscrtpwr"
client.username_pw_set(user, password)
client.on_connect = on_connect
client.on_message = on_message


class tMqtt(threading.Thread):    
    def  __init__( self ):    
        super(tMqtt,  self ).__init__()
        self.x=0
        self.y=0
        self.z=0
        self.lock=True
    def  run( self ):    
        try:    
            client.connect("10.42.0.1", 1883, 10)  
            client.loop_forever()  
        except KeyboardInterrupt:  
            client.disconnect()

thread=tMqtt()
thread.start()

#plotting(webgl is gpu supported version)
p = figure(plot_width=1000, plot_height=600)
#p = figure(plot_width=1000, plot_height=600, output_backend="webgl")
p.x_range.follow="end"
p.x_range.follow_interval = 300
p.x_range.range_padding=0
r1 = p.line([], [], color="firebrick", line_width=2)
r2 = p.line([], [], color="navy", line_width=2)
r3 = p.line([], [], color="green", line_width=2)

ds1 = r1.data_source
ds2 = r2.data_source
ds3 = r3.data_source

@linear()
def update(step):
    global count
    global cur
    if thread.lock is False:
        thread.lock=True
        count+=1
        if time.time()-cur>1:
            print("Data Rate:\t",count)
            count=0
            cur=time.time()
        ds1.data['x'].append(step)
        ds1.data['y'].append(thread.x)
        ds2.data['x'].append(step)
        ds2.data['y'].append(thread.y)
        ds3.data['x'].append(step)
        ds3.data['y'].append(thread.z)  
        if len(ds1.data['x']) >=300:
            ds1.data['x'].pop(0)
            ds1.data['y'].pop(0)
        if len(ds2.data['x']) >=300:
            ds2.data['x'].pop(0)
            ds2.data['y'].pop(0)
        if len(ds3.data['x']) >=300:
            ds3.data['x'].pop(0)
            ds3.data['y'].pop(0)
        ds1.trigger('data', ds1.data, ds1.data)
        ds2.trigger('data', ds2.data, ds2.data)
        ds3.trigger('data', ds3.data, ds3.data)

curdoc().add_root(p)

# Add a periodic callback to be run every 500 milliseconds
curdoc().add_periodic_callback(update, 10)