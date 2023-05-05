# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 19:24:34 2021

@author: USER
"""
import numpy as np
from PIL import Image

""""
(159,56), (388,81), (159,396), (387, 380)
"""


x1 = 159
y1 = 56
x2 = 388
y2 = 81
x3 = 159
y3 = 396
x4 = 387
y4 = 380
""""
(0,0), (224,0),(0,224), (224, 224)
"""

p1 = 0
q1 = 0
p2 = 224
q2 = 0
p3 = 0
q3 = 224
p4 = 224
q4 = 224

A = np.zeros((8,8))
b = np.zeros((8,1))
A[0,:] = [x1,y1,1,0,0,0,-p1*x1,-p1*y1]
A[1,:] = [x2,y2,1,0,0,0,-p2*x2,-p2*y2]
A[2,:] = [x3,y3,1,0,0,0,-p3*x3,-p3*y3]
A[3,:] = [x4,y4,1,0,0,0,-p4*x4,-p4*y4]
A[4,:] = [0,0,0,x1,y1,1,-q1*x1,-q1*y1]
A[5,:] = [0,0,0,x2,y2,1,-q2*x2,-q2*y2]
A[6,:] = [0,0,0,x3,y3,1,-q3*x3,-q3*y3]
A[7,:] = [0,0,0,x4,y4,1,-q4*x4,-q4*y4]
b[:,0] = [p1,p2,p3,p4,q1,q2,q3,q4]

x = np.linalg.lstsq(A,b)[0]

H = np.zeros((3,3))
H[0,0] = x[0]
H[0,1] = x[1]
H[0,2] = x[2]
H[1,0] = x[3]
H[1,1] = x[4]
H[1,2] = x[5]
H[2,0] = x[6]
H[2,1] = x[7]
H[2,2] = 1

print(H)
BG = Image.open('BG.jpg')
BG_data = np.asarray(BG).copy()
I = Image.open('KO.jpg')
data = np.asarray(I)
[H1,W1,t] = BG_data.shape
[H2,W2,t] = data.shape
xy1 = np.ones((3,1))
pq1 = np.zeros((3,1))
for h in range(H1):
    for w in range(W1):
        xy1[0] = w
        xy1[1] = h
        pq1 = np.dot(H,xy1)
        p = int(pq1[0][0]/pq1[2][0])
        q = int(pq1[1][0]/pq1[2][0])
        if(p>=0 and p<W2 and q>=0 and q<H2):
            BG_data[h,w,:] = data[q,p,:]
I2 = Image.fromarray(BG_data)
I2.show()
        