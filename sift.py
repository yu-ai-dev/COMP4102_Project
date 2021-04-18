# Jiaming Mei
# 101014538

import numpy as np
import cv2
from matplotlib import pyplot as plt

import segment

def siftMatch(input, sign, threshold=0.75):

    if(input.shape[0] < 50 or input.shape[1] < 50):
        return 0

    img1 = sign
    img2 = input
    #img2 = cv2.imread('testS.png')

    #img2 = segment.colorRedSegment(img2)

    # img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # img2 = cv2.cvtColor(img2, cv2.COLOR_HSV2RGB)
    # img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)

    #detector = cv2.AKAZE_create()
    detector = cv2.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = detector.detectAndCompute(img1, None)
    kp2, des2 = detector.detectAndCompute(img2, None)



    # create BFMatcher object
    #bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    bf = cv2.BFMatcher()


    matches = bf.knnMatch(des1,des2, k=2)

    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < threshold*n.distance:
            good.append([m])

    # cv2.drawMatchesKnn expects list of lists as matches.
    #img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None, flags=2)

    #plt.imshow(img3),plt.show()



    # Sort them in the order of their distance.
    #matches = sorted(matches, key = lambda x:x.distance)
    #print(len(good))


    #cv2.imshow('Matches', img3)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return len(good)

# img1 = cv2.imread("stop2_red.png")
# img2 = cv2.imread("stopData.png")
# siftMatch(img1, img2)
