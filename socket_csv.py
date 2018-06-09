import socket
import time

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

while 1:
    data = conn.recv(4096) #Receives data in chunks
    if '*' in data: #When end of data is received
        break
    dataList += data

fwrite = open('./10Hz_50_Z_1.csv','w')
# except KeyboardInterrupt:
fwrite.write('x_voltage,y_voltage,z_voltage,x_gvalue,y_gvalue,z_gvalue,time'+'\n')
for line in dataList.split("#"):
    if len(line) > 5 :
        splitData = line.split("&")
        sensorValue = eval(splitData[1])
        timestamp = splitData[0]
        acc = computeAcc(sensorValue)
        fwrite.write('NA,NA,NA,')
        for i in range(3):
            fwrite.write("%f,"%float(acc[i]))
        fwrite.write(timestamp + "\n")