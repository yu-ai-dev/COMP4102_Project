import numpy as np
import cv2

def colorRedSegment(input, threshold = 5):

    hsv = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0,30,100])
    upper_red = np.array([10,255,255])

    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170,30,100])
    upper_red = np.array([180,255,255])

    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask = mask1 + mask2

    #mask = cv2.blur(mask, (5, 5))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (threshold, threshold))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    res = cv2.bitwise_and(input,input, mask= mask)


    pixels = cv2.findNonZero(mask)

    left = min(pixels, key=lambda x: x[0][1])[0][1]
    right = max(pixels, key=lambda x: x[0][1])[0][1]
    top = min(pixels, key=lambda x: x[0][0])[0][0]
    bottom = max(pixels, key=lambda x: x[0][0])[0][0]



    crop = res[left:right, top:bottom]
    cv2.imshow('mask', mask)




    return crop


def testRun():

    imgInput = cv2.imread('test.jpg')
    #print(imgInput)

    cv2.imshow('frame',imgInput)
    #cv2.imshow('mask',mask)
    res = colorRedSegment(imgInput)
    cv2.imshow('res',res)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

#testRun()
