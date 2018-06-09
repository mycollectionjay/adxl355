from bokeh.plotting import figure, output_file, show
from scipy.fftpack import fft, dst, idst
import numpy as np
import random
import pickle
import csv
import os
import random
import operator
import pickle
from scipy import signal

######################Utils function######################

def findDirs(dirs, ext=None):
    ret_list=[]
    if type(dirs) == list:
        for p in dirs:
            if os.path.isdir(p):
                datapath=os.listdir(p)
                files_arr=[]
                dirs_arr=[]
                for target in datapath:
                    target=p+'/'+target
                    if os.path.isfile(target):
                        files_arr.append(target)
                    if os.path.isdir(target):
                        dirs_arr.append(target)
                if len(dirs_arr) > 0:
                    ret_list+=findDirs(dirs_arr, ext)
                if len(files_arr) > 0:
                    ret_list+=findFiles(files_arr, ext)
            else:
                print "Directory:", p, "not found!"
                
    elif type(dirs) == str:
        if os.path.isdir(dirs):
            datapath=os.listdir(dirs)
            files_arr=[]
            dirs_arr=[]
            for target in datapath:
                target=dirs+'/'+target
                if os.path.isfile(target):
                    files_arr.append(target)
                if os.path.isdir(target):
                    dirs_arr.append(target)
            if len(dirs_arr) > 0:
                ret_list+=findDirs(dirs_arr, ext)
            if len(files_arr) > 0:
                ret_list+=findFiles(files_arr, ext)
        else:
            print "Directory:", dirs, "not found!"
    else:
        print "wrong argument format!!!"

    return ret_list


def findFiles(files, ext=None):
    if type(files) == str:
        if os.path.isfile(files):
            return files
        else:
            print "'" + files + "' file not found"
            return None
    elif type(files) == list:
        ret_list=[]
        for target in files:
            if os.path.isfile(target):
                part=target.split(".")
                if part[len(part)-1]==ext or ext==None:
                    ret_list.append(target)
            else:
                print "'" + target + "' file not found"

        return ret_list
    else:
        print "input should be either list or string"

######################Kmeans######################
def distance(f1, f2):
    xf1 = np.pad(f1[1], (10,10), 'constant')
    yf1 = np.pad(f1[2], (10,10), 'constant')
    zf1 = np.pad(f1[3], (10,10), 'constant')
    xf2 = f2[1]
    yf2 = f2[2]
    zf2 = f2[3]
    if xf1==None or xf2==None:
        print "BUG",xf1, " ", xf2
    corrx=signal.correlate(xf1, xf2, mode='valid', method='direct')
    corry=signal.correlate(yf1, yf2, mode='valid', method='direct')
    corrz=signal.correlate(zf1, zf2, mode='valid', method='direct')
    return 1.0/(max(corrx)**2+max(corry)**2+max(corrz)**2)
    # return -1*(sum(corrx) + sum(corry) + sum(corrz))

def kMeans(fq_arr, k):
    assert(k<=len(fq_arr))
    assert(k>0)

    centers=[]
    clusters=[]
    iter=20

    # initial centroids estimation(kmeans++)
    fqCpy=fq_arr[:]
    centers=[]
    random.shuffle(fqCpy)
    centers.append(fqCpy.pop(0))
    for it in range(k-1):
        maxDistance=0
        tmpid=None
        for it2 in range(len(fqCpy)):
            tmpDist=0
            for c in centers:
                tmpDist+=distance(c, fqCpy[it2])
            if tmpid==None:
                tmpid=it2
                maxDistance=tmpDist    
            elif maxDistance<tmpDist:
                tmpid=it2
                maxDistance=tmpDist
        centers.append(fqCpy.pop(it2))
    
    print "CENTERS:  ", [c[0] for c in centers]
    # standard kmeans
    # print"CENTERS ", centers
    delta_old=1000000000000
    while True:
        clusters=[[] for c in range(k)]
        for fq in fq_arr:
            minDistance=100000000000000000000000
            bestGroup=None
            for c in range(k):
                dist=distance(fq,centers[c])
                # print "DIST ",dist
                if dist < minDistance:
                    bestGroup=c
                    minDistance=dist
            clusters[bestGroup].append(fq)
        # for c in range(len(clusters)):
        #     print "cluster ",c ,": ", len(clusters[c])
        newCenters=[]
        for c in range(k):
            xf=None
            yf=None
            zf=None
            name="center"
            size=float(len(clusters[c]))
            for fq in clusters[c]:
                if xf is None:
                    xf=fq[1]/size
                    yf=fq[2]/size
                    zf=fq[3]/size
                else:
                    xf=xf+fq[1]/size
                    yf=yf+fq[2]/size
                    zf=zf+fq[3]/size
            newCenters.append((name, xf, yf, zf))
        delta=0
        print len(centers), ' ', len(newCenters)
        for it in range(k):
            delta+=distance(centers[it], newCenters[it])
        if delta_old==delta:
            break
        delta_old=delta
        # iter-=1
        # if iter<=0:
        #     break
            
    return clusters, centers

######################MAIN######################

fq_arr=[]
files=findDirs("simulate")
print files
for f in files:
    x=[]
    y=[]
    z=[]
    read=open(f, 'r')
    for row in csv.DictReader(read):
        # print "x: ", row['x_gvalue'], "\t\ty: ", row['y_gvalue'], "\t\tz: ", row['z_gvalue'], "\t\ttime: ", row['time']
        x.append(float(row['x_gvalue']))    
        y.append(float(row['y_gvalue']))
        z.append(float(row['z_gvalue']))
        
    x_zero = sum(x[:200])/200.0
    y_zero = sum(y[:200])/200.0
    z_zero = sum(z[:200])/200.0

    x = [(d-x_zero) for d in x]
    y = [(d-y_zero) for d in y]
    z = [(d-z_zero) for d in z]

    xf=(abs(dst(x, type=1))/len(x))
    yf=(abs(dst(y, type=1))/len(y))
    zf=(abs(dst(z, type=1))/len(z))

    fq_arr.append((f, xf, yf, zf))

clusters, centers=kMeans(fq_arr, 2)
for i in range(len(clusters)):
    print"clusters", i
    for j in clusters[i]:
        print "\t", j[0]
    print ""