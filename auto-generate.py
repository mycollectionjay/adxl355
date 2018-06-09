from bokeh.plotting import figure, output_file, show
from scipy.fftpack import fft, dst, idst
import numpy as np
import random
import pickle
import csv

# x=np.linspace(0,1,1000)
# y=6*np.sin(2*np.pi*10*x)

numData=int(raw_input("Number of datas to be generated: "))

for it in range(numData):
    print "data ", it+1
    freq=float(raw_input("frequency: "))
    amp=float(raw_input("amplitude: "))
    axis=int(raw_input("x(0)/y(1)/z(2): "))
    x=np.linspace(0,10,2000)
    x_interference=np.random.random_sample(2000)/1000
    x=x+x_interference
    y=amp*np.sin(2*np.pi*freq*x)
    y_interference=np.random.random_sample(2000)/100
    y=y+y_interference
    interference1=np.random.random_sample(2000)/50
    interference2=np.random.random_sample(2000)/50
    print interference1[:100]

    # write file
    fwrite=open(str(freq)+'hz_'+str(amp)+'g_'+str(it)+'.csv', 'w')
    fields=["x_gvalue", "y_gvalue", "z_gvalue", "time"]
    writer=csv.DictWriter(fwrite, fieldnames=fields)
    writer.writeheader()
    for it2 in range(2000):
        d={"x_gvalue":y[it2], "y_gvalue":interference1[it2], "z_gvalue":interference2[it2], "time":x[it2]}
        if axis==1:
            d["y_gvalue"]=y[it2]
            d["x_gvalue"]=interference1[it2]
        elif axis==2:
            d["z_gvalue"]=y[it2]
            d["x_gvalue"]=interference2[it2]
        writer.writerow(d)

