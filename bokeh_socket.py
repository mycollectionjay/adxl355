# myplot.py
from bokeh.layouts import row,column, gridplot
from bokeh.models import ColumnDataSource, Slider, Select
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
import threading
import socket
import time

class Buffer(object):
    count=0
    start=0
    step=[]
    x=[]
    y=[]
    z=[]

def computeAcc(sensorValue):
    acc = [[] for i in range(3)]
    for i in range(3):
        sensorValue[i][0] *= 256*16
        sensorValue[i][1] *= 16
        sensorValue[i][2] &= 240
        sensorValue[i][2] /= 16
        acc[i] = float(sum(sensorValue[i]))
    for i in range(3):
        if acc[i] >= 524288:
            acc[i] = acc[i] - 1048576
        acc[i] = (acc[i]/524288.0)*2.048
    return acc

class tSocket(threading.Thread):    
    def __init__( self ):    
        super(tSocket,  self ).__init__()

    def run( self ):    
        try:    
            HOST = '10.42.0.1'
            PORT = 50007
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            procno = 2
            s.listen(procno - 1) #Listens for (n) number of client connections
            print 'Waiting for client...'
            addr_list = []

            for i in range(procno - 1): #Connects to all clients
                conn, addr = s.accept() #Accepts connection from client
                print 'Connected by', addr
                addr_list.append(addr) #Adds address to address list

            dataList=""

            initial=None
            Buffer.start=time.time()
            while 1:
                data = conn.recv(1024) #Receives data in chunks
                if '*' in data: #When end of data is received
                    break
            
                for line in data.split("#"):
                    if len(line) > 5 :
                        splitData = line.split("&")
                        try:
                            sensorValue = eval(splitData[1])
                        except:
                            print(data)
                            continue
                        timestamp = float(splitData[0])
                        acc = computeAcc(sensorValue)
                        Buffer.x.append(acc[0])
                        Buffer.y.append(acc[1])
                        Buffer.z.append(acc[2])
                        if initial==None:
                            initial=timestamp
                        Buffer.step.append(timestamp-initial)
                        
        except KeyboardInterrupt:
            self.terminate()

thread=tSocket()
thread.start()

source=ColumnDataSource(dict(time=[], x=[], y=[], z=[]))
#plotting(webgl is gpu supported version)
p = figure(plot_width=1000, plot_height=600)
#p = figure(plot_width=1000, plot_height=600, output_backend="webgl")
p.x_range.follow="end"
p.x_range.follow_interval = 1000
p.x_range.range_padding=0
p.min_border_left = 40
p.min_border_bottom = 20
r1 = p.line(x='time', y='x', color="firebrick", line_width=2, source=source)
r2 = p.line(x='time', y='y', color="navy", line_width=2, source=source)
r3 = p.line(x='time', y='z', color="green", line_width=2, source=source)


def update():
    if Buffer.step!=[]:
        iterate=min(len(Buffer.step), len(Buffer.x), len(Buffer.y), len(Buffer.z))
        for it in range(iterate):
            Buffer.count+=1
            new_data=dict(time=[Buffer.step.pop(0)], x=[Buffer.x.pop(0)], y=[Buffer.y.pop(0)], z=[Buffer.z.pop(0)])
            source.stream(new_data, 1000)
            
            if Buffer.count==2000:
                print "Total time: ",time.time()-Buffer.start
                Buffer.count=0
                Buffer.start=time.time()
           

#######################################
curdoc().add_root(p)
curdoc().add_periodic_callback(update, 50)

# # Add a periodic callback to be run every 500 milliseconds
# curdoc().add_periodic_callback(update, 10)