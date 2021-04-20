import cv2
import numpy as np
import sys
from stackImages import *

def getContour(input, output, area_threshold):
    contours, hierarchy = cv2.findContours(input, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    img = output.copy()


    x,y,w,h = 0, 0, img.shape[0]-1, img.shape[1]-1
    count = 0
    for cout in contours:
        area = cv2.contourArea(cout)
        if(area > area_threshold):
            count += 1
            cv2.drawContours(output, cout, -1, (0, 255,0), 2)
            x,y,w,h = cv2.boundingRect(cout)
            cv2.rectangle(output,(x,y),(x+w,y+h),(255,140,0),2)


    if(y+h >= img.shape[0] or x+w >= img.shape[1]):
        return img

    cropped = img[y:y+h-1, x:x+w-1]



    return cropped




def cropContour(input, mask, blur=2, cannyMin=160, cannyMax=255, dilate=2, area=30):

    #gray = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
    #imgBlur = cv2.GaussianBlur(gray, (2*blur+1, 2*blur+1), 1)
    imgCanny = cv2.Canny(mask, cannyMin, cannyMax)
    imgDil = cv2.dilate(imgCanny, np.ones((dilate, dilate)))
    imgContour = input.copy()
    cropped = getContour(imgDil, imgContour, area*100)

    return cropped


def run(input_name):

    img = cv2.imread(input_name)

    def empty(x):
        pass

    cv2.namedWindow("Trackbar")
    cv2.createTrackbar("Blur", "Trackbar", 0, 6, empty)
    cv2.createTrackbar("Canny Min", "Trackbar", 20, 255, empty)
    cv2.createTrackbar("Canny Max", "Trackbar", 20, 255, empty)
    cv2.createTrackbar("Dilate", "Trackbar", 1, 9, empty)
    cv2.createTrackbar("Area", "Trackbar", 1, 40, empty)

    while(1):

        blur = cv2.getTrackbarPos("Blur", "Trackbar")
        cannyMin = cv2.getTrackbarPos("Canny Min", "Trackbar")
        cannyMax = cv2.getTrackbarPos("Canny Max", "Trackbar")
        dilate = cv2.getTrackbarPos("Dilate", "Trackbar")
        area = cv2.getTrackbarPos("Area", "Trackbar")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        imgBlur = cv2.GaussianBlur(gray, (2*blur+1, 2*blur+1), 1)

        imgCanny = cv2.Canny(imgBlur, cannyMin, cannyMax)

        imgDil = cv2.dilate(imgCanny, np.ones((dilate, dilate)))

        imgContour = img.copy()
        cropped = getContour(imgDil, imgContour, area*100)

        imgStack = stackImages(([img, imgBlur, imgCanny], [imgDil, imgContour, cropped]), 0.1)
        cv2.imshow("Result", imgStack)
        #cv2.resizeWindow("Result", 800, 800)
        cv2.imwrite("Cropped.png", cropped)



        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break


    cv2.destroyAllWindows()

if __name__ == "__main__":

    if len(sys.argv) >1:
        read_image = sys.argv[1]
        run(read_image)
