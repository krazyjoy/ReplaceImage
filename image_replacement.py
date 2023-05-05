# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 19:24:34 2021

@author: USER
"""
import numpy as np
import cv2
"""
1357 x 727 (寬x高)


左上, 右上,左下, 右下
((496,493),(764,473),(558,707), (887,677))


"""
x1 = 496
y1 = 493
x2 = 764
y2 = 473
x3 = 558
y3 = 707
x4 = 887
y4 = 677

"""
500 x 500 (寬x高)


左上, 右上, 左下, 右下
((0,0),(499,0), (0,499), (499,499))


"""

p1 = 0
q1 = 0
p2 = 499
q2 = 0
p3 = 0
q3 = 499
p4 = 499
q4 = 499

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
b[:,0] = [p1,p2,p3,p4,q1,q2,q3,q4] # (x1',x2',x3',x4',y1',y2',y3',y4')

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

BG = cv2.imread('background.png')
BG_data = BG.copy()
I = cv2.imread('dinosaur.jpg')
data = np.asarray(I)
[H1,W1,t] = BG_data.shape # [727, 1357, 3]
[H2,W2,t] = data.shape # [500, 500, 3]
print("BG_DATA:\n",BG_data[1,1,:])
# find transform matrix for target-image(dinosaur)
"""
[p,q,1] = [[h1,h2,h3],   *  [x,y,1]
           [h4,h5,h6],
           [h7,h8,h9]]
"""
xy1 = np.ones((3,1))
pq1 = np.zeros((3,1))
for h in range(H1):
    for w in range(W1):
        xy1[0] = w
        xy1[1] = h
        pq1 = np.dot(H,xy1) # transform background image points to dinosaur canvas
        #print("pq1",pq1) # [3,1]
        p = int(pq1[0][0]/pq1[2][0]) # width = y
        q = int(pq1[1][0]/pq1[2][0]) # height = x
        if(p>=0 and p<W2 and q>=0 and q<H2): # if points belongs inside dinosaur canvas then map points from dinosaur to bg image
            print("matched")
            # print(data[q,p,:])
            # print(BG_data[h,w,:])
            BG_data[h,w,:] = data[q,p,:]
I2 = cv2.imwrite("new_BG2.png",BG_data)
I2 = cv2.imread("new_BG2.png")
cv2.imshow("new background:",I2)
cv2.waitKey(0)
cv2.destroyAllWindows()
        