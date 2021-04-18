import cv2
import numpy as np

#load image
img=cv2.imread('test2.jpg')
print('img:',type(img),img.shape,img.dtype)
# cv2.imshow('img',img)

hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# cv2.imshow('hsv',hsv)

#get the blue area
blue_lower=np.array([100,50,50])
blue_upper=np.array([124,255,255])
mask=cv2.inRange(hsv,blue_lower,blue_upper)
print('mask',type(mask),mask.shape)
# cv2.imshow('mask',mask)


blurred=cv2.blur(mask,(9,9))
# cv2.imshow('blurred',blurred)
#Binary
ret,binary=cv2.threshold(blurred,127,255,cv2.THRESH_BINARY)
# cv2.imshow('blurred binary',binary)

#Close the area without gaps
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
# cv2.imshow('closed',closed)


erode=cv2.erode(closed,None,iterations=4)
# cv2.imshow('erode',erode)
dilate=cv2.dilate(erode,None,iterations=4)
# cv2.imshow('dilate',dilate)


contours, hierarchy=cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

i=0
res=img.copy()
for con in contours:
    #to rectangle
    rect=cv2.minAreaRect(con)
    #change rectangle to the box
    box=np.int0(cv2.boxPoints(rect))
    #draw the area
    cv2.drawContours(res,[box],-1,(0,0,255),2)
    print([box])
    #calculate the rectangle
    h1=max([box][0][0][1],[box][0][1][1],[box][0][2][1],[box][0][3][1])
    h2=min([box][0][0][1],[box][0][1][1],[box][0][2][1],[box][0][3][1])
    l1=max([box][0][0][0],[box][0][1][0],[box][0][2][0],[box][0][3][0])
    l2=min([box][0][0][0],[box][0][1][0],[box][0][2][0],[box][0][3][0])
    print('h1',h1)
    print('h2',h2)
    print('l1',l1)
    print('l2',l2)

    if h1-h2>0 and l1-l2>0:
        temp=img[h2:h1,l2:l1]
        i=i+1
        #image after cuts
        # cv2.imshow('sign'+str(i),temp)
#draw the original image
cv2.imshow('res',res)

cv2.waitKey(0)
cv2.destroyAllWindows()
