import numpy as np
import cv2
import sys
import os

def initColor():

    color_filter = dict()
    color_filter["red"] = [([0,30,100], [10,255,255]), ([170,30,100], [180,255,255])]
    color_filter["yellow"] = [([22, 93, 0], [45, 255, 255])]
    color_filter["blue"] = [([60, 35, 140], [180, 255, 255])]

    return color_filter

def segment(input, color, threshold = 5):

    color_filter = initColor()

    segmented_list = []

    if(color == "all"):
        for cf in color_filter:
            sm = colorSegment(input, str(cf), threshold)
            segmented_list.append((cf, sm))
    elif(color in color_filter):
        sm = colorSegment(input, color, threshold)
        segmented_list.append((color, sm))
    else:
        print(" Need proper color name")

    return segmented_list



def colorSegment(input, color, threshold = 5):


    color_filter = initColor()

    original = input.copy()

    input = cv2.GaussianBlur(input, (7, 7), 1)

    hsv = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)

    color_hsv = color_filter[color]

    masks = []
    for c in color_hsv:
        lower = np.array(c[0])
        upper = np.array(c[1])
        m = cv2.inRange(hsv, lower, upper)
        masks.append(m)

    if(len(masks)>0):
        mask = masks[0]
    for m in masks:
        mask = mask + m


    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (threshold, threshold))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    res = cv2.bitwise_and(input,input, mask= mask)


    pixels = cv2.findNonZero(mask)

    left, right, top, bottom = 0, 1, 0, 1



    if(pixels is None):
        return input, np.zeros_like(original)

    left = min(pixels, key=lambda x: x[0][1])[0][1]
    right = max(pixels, key=lambda x: x[0][1])[0][1]
    top = min(pixels, key=lambda x: x[0][0])[0][0]
    bottom = max(pixels, key=lambda x: x[0][0])[0][0]


    crop = original[left:right, top:bottom]


    return original, mask




def run(input_name, color):

    imgInput = cv2.imread(input_name)
    #print(imgInput)

    if(not os.path.exists(os.path.join(os.getcwd(), "SegmentTest"))):
        os.makedirs(os.path.join(os.getcwd(), "SegmentTest"))

    #cv2.imshow('Image',imgInput)

    segmented_list = segment(imgInput, color)
    for i in segmented_list:
        cv2.imshow(str(i[0]),i[1][0])
        cv2.imshow(str(i[0])+"mask", i[1][1])
        cv2.imwrite(os.path.join(os.getcwd(), "SegmentTest", str(i[0])+".png"), i[1][0])
        cv2.imwrite(os.path.join(os.getcwd(), "SegmentTest", str(i[0])+"_mask.png"), i[1][1])

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if len(sys.argv) >1:
    read_image = sys.argv[1]
    color = "all"
    if(len(sys.argv) >2):
        color = str(sys.argv[2])
    run(read_image, color)
