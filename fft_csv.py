from bokeh.plotting import figure, output_file, show
from scipy.fftpack import fft, dst, idst
import numpy as np
import random
import pickle
import csv

time=[]
x=[]
y=[]
z=[]
f=open("../data/5Hz_500_Y_1.csv", 'r')
# f=open("../data/5Hz_500_X_1.csv", 'r')
for row in csv.DictReader(f):
    # print "x: ", row['x_gvalue'], "\t\ty: ", row['y_gvalue'], "\t\tz: ", row['z_gvalue'], "\t\ttime: ", row['time']
    x.append(float(row['x_gvalue']))    
    y.append(float(row['y_gvalue']))
    z.append(float(row['z_gvalue']))
    time.append(float(row['time']))

x_zero = sum(x)/len(x)
y_zero = sum(y)/len(y)
z_zero = sum(z)/len(z)
# print x_zero
# print y_zero
# print z_zero

initial=time[0]
x = [(d-x_zero) for d in x]
y = [(d-y_zero) for d in y]
z = [(d-z_zero) for d in z]
time=[(d-initial) for d in time]

xf=abs(dst(x, type=1))/len(time)
yf=abs(dst(y, type=1))/len(time)
zf=abs(dst(z, type=1))/len(time)
N=float(len(time))
T=float(time[len(time)-1]-time[0])/N
print "N: ", N, "\t\tT: ", T
timef=np.linspace(0.0, 1.0/(2.0*T), len(time))
p = figure(plot_width=1000, plot_height=600)
p.min_border_left = 40
p.min_border_bottom = 20
p.line(timef[:1000], xf[:1000], color="firebrick", line_width=2)
p.line(timef[:1000], yf[:1000], color="navy", line_width=2)
p.line(timef[:1000], zf[:1000], color="green", line_width=2)

show(p)
f.close()