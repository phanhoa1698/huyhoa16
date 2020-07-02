#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys,os
import numpy as np
from math import * 
from PIL import Image
import shutil


# # Preprocess Data

# filenames=['FDDB-fold-01.txt','FDDB-fold-02.txt','FDDB-fold-03.txt','FDDB-fold-04.txt',
#           'FDDB-fold-05.txt','FDDB-fold-06.txt','FDDB-fold-07.txt','FDDB-fold-08.txt'
#           ,'FDDB-fold-09.txt','FDDB-fold-10.txt']
# with open ('FDDBimagepath.txt','w') as outfile:
#     for fname in filenames:
#         with open(fname)as infile :
#             outfile.write(infile.read())

# In[ ]:


filenames=['FDDB-fold-01-ellipseList.txt','FDDB-fold-02-ellipseList.txt','FDDB-fold-03-ellipseList.txt','FDDB-fold-04-ellipseList.txt',
          'FDDB-fold-05-ellipseList.txt','FDDB-fold-06-ellipseList.txt','FDDB-fold-07-ellipseList.txt','FDDB-fold-08-ellipseList.txt'
          ,'FDDB-fold-09-ellipseList.txt','FDDB-fold-10-ellipseList.txt']
with open ('FDDBimage_ellipse.txt','w') as outfile:
    for fname in filenames:
        with open(fname)as infile :
            outfile.write(infile.read())


# In[9]:


imagepath_filename='FDDBimagepath.txt'
with open(imagepath_filename)as f:
    lines=[line.rstrip('\n') for line in f] 
def getimagename(line):
    x=line.split("img")
    y=x[0]
    return y
i=0
while i<len(lines):
    img_file='../ori/' + lines[i] +'.jpg'
    des_path='../pic/'+ getimagename(lines[i])
    if not os.path.exists(des_path):
        os.makedirs(des_path)
    shutil.copy(img_file ,des_path)
    print ('done'+'%s' %i )
    i=i+1
f.close()


# In[10]:


def filter (c,m):
    if c<0:
        return 0 
    elif c>m:
        return m 
    else :
        return c
def getimagename(line):
    x=line.split(".")
    y='img_'+x[1]
    return y
elipse_filename='FDDBimage_ellipse.txt'
with open(elipse_filename) as f:
    lines=[line.rstrip('\n') for line in f]
i=0
while i<len(lines):
    img_file='../pic/'+ lines[i]+'.jpg'
    rect_filename='../pic/'+lines[i]+'.txt'
    f=open(rect_filename,'w')
    img=Image.open(img_file)
    w=img.size[0]
    h=img.size[1]
    num_faces=int(lines[i+1])
    for j in range(num_faces):
        ellipse=lines[i+2+j].split()[0:5]
        a = float(ellipse[0])
        b = float(ellipse[1])
        angle = float(ellipse[2])
        centre_x = float(ellipse[3])
        centre_y = float(ellipse[4])

        tan_t = -(b/a)*tan(angle)
        t = atan(tan_t)
        x1 = centre_x + (a*cos(t)*cos(angle) - b*sin(t)*sin(angle))
        x2 = centre_x + (a*cos(t+pi)*cos(angle) - b*sin(t+pi)*sin(angle))
        x_max = filter(max(x1,x2),w)
        x_min = filter(min(x1,x2),w)

        if tan(angle) != 0:
            tan_t = (b/a)*(1/tan(angle))
        else:
            tan_t = (b/a)*(1/(tan(angle)+0.0001))
        t = atan(tan_t)
        y1 = centre_y + (b*sin(t)*cos(angle) + a*cos(t)*sin(angle))
        y2 = centre_y + (b*sin(t+pi)*cos(angle) + a*cos(t+pi)*sin(angle))
        y_max = filter(max(y1,y2),h)
        y_min = filter(min(y1,y2),h)
        m= (x_max+x_min)/2
        n= (y_max + y_min)/2
        x=m/w
        y=n/h
        w1= (x_max-x_min)/w
        h1=(y_max-y_min)/h
        text = '0' + ' '+str(x)+' '+str(y)+' '+str(w1)+' '+str(h1)+'\n'
        f.write(text)
    i = i + num_faces + 2
f.close()


# # Using Yolo_V3 To train the program
