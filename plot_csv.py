from bokeh.plotting import figure, output_file, show
from bokeh.driving import linear
import random
import pickle
import csv

time=[]
x=[]
y=[]
z=[]
f=open("data/5Hz_500_X_1.csv", 'r')
for row in csv.DictReader(f):
    # print "x: ", row['x_gvalue'], "\t\ty: ", row['y_gvalue'], "\t\tz: ", row['z_gvalue'], "\t\ttime: ", row['time']
    x.append(row['x_gvalue'])    
    y.append(row['y_gvalue'])
    z.append(row['z_gvalue'])
    time.append(float(row['time']))

output_file("plot.html", mode="inline")

initial=time[0]
time=[d-initial for d in time]
p = figure(plot_width=1000, plot_height=600)
p.line(time, x, color="firebrick", line_width=2)
p.line(time, y, color="navy", line_width=2)
p.line(time, z, color="green", line_width=2)

show(p)
f.close()
