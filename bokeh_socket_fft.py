# myplot.py
#from bokeh.layouts import row,column, gridplot
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
from scipy.fftpack import fft, dst, idst
import threading
import socket
import time

class Buffer(object):
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
            while 1:
                data = conn.recv(512) #Receives data in chunks
                if '*' in data: #When end of data is received
                    break
            
                for line in data.split("#"):
                    if len(line) > 5 :
                        splitData = line.split("&")
                        try:
                            sensorValue = eval(splitData[1])    
                        except:
                            print "ERROR"
                            continue
                        timestamp = float(splitData[0])
                        acc = computeAcc(sensorValue)
                        Buffer.x.append(acc[0])
                        Buffer.y.append(acc[1])
                        Buffer.z.append(acc[2])
                        if initial==None:
                            initial=timestamp
                        Buffer.step.append(timestamp-initial)
                if len(Buffer.step)>1000:
                    Buffer.x=Buffer.x[-1000:]
                    Buffer.y=Buffer.y[-1000:]
                    Buffer.z=Buffer.z[-1000:]
                    Buffer.step=Buffer.step[-1000:]
                        
        except KeyboardInterrupt:
            self.terminate()

thread=tSocket()
thread.start()

#plotting(webgl is gpu supported version)
p = figure(plot_width=1000, plot_height=600)
p.min_border_left = 40
p.min_border_bottom = 20
#p = figure(plot_width=1000, plot_height=600, output_backend="webgl")
r1 = p.line([], [], color="firebrick", line_width=2)
r2 = p.line([], [], color="navy", line_width=2)
r3 = p.line([], [], color="green", line_width=2)

ds1 = r1.data_source
ds2 = r2.data_source
ds3 = r3.data_source

def update():
    if len(Buffer.step)>=1000:
        i=Buffer.step[-1000]
        steps=[s-i for s in Buffer.step[-1000:]]

        xf=abs(dst(Buffer.x[-1000:], type=1))/1000
        yf=abs(dst(Buffer.y[-1000:], type=1))/1000
        zf=abs(dst(Buffer.z[-1000:], type=1))/1000
        ds1.data['x']=steps[:100]
        ds1.data['y']=xf[:100]
        ds2.data['x']=steps[:100]
        ds2.data['y']=yf[:100]
        ds3.data['x']=steps[:100]
        ds3.data['y']=zf[:100]

        ds1.trigger('data', ds1.data, ds1.data)
        ds2.trigger('data', ds2.data, ds2.data)
        ds3.trigger('data', ds3.data, ds3.data)
    else:
        print len(Buffer.step), len(Buffer.x), len(Buffer.y), len(Buffer.z)
            
           

#######################################
curdoc().add_root(p)
curdoc().add_periodic_callback(update, 50)

# # Add a periodic callback to be run every 500 milliseconds
# curdoc().add_periodic_callback(update, 10)