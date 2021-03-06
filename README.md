# COMP4102_Project

Final project for COMP4102A: Computer Vision in winter 2021.

## Project Title
Traffic Sign Recognition

## Summary
Traffic Sign Recognition is to recognize and identify the traffic signs in Canada. The project needs to deal with image processing (shape and color processing)  and image recognition (text and symbol recognition).

## Background
There are existing multiple car brands that support traffic sign recognition in technology. The whole technique aims to recognize the traffic sign information with the car front-facing cameras and translate the instructions to the drivers and cars controller to improve driving behaviors and reduce the number of traffic accidents. OpenCV is the primary tool to achieve image reconstruction, image segmentation, and shape recognition in the traffic sign recognition system. Programming is also required in Python to proceed with database implementation, data matching, and error computation. Our project lays emphasis on the correctness and accuracy of the recognition while giving up the goal of recognition and processing speed. 

## The Challenge
There are two main challenges in the project. The one is shape and color recognition that contains fuzzy images, image noise, and image brightness… The other is content recognition, which includes traffic template matching, text recognition, and error analysis... All the image processing operations, feature extraction, and object detection problems can be solved using OpenCV functions. And all the image database matching and error analysis can be achieved by Python and algorithms. We are hoping to learn the basics of image formation through the project and use tools like OpenCV to proceed with image processing under multiple requirements. We expect to use the programming language to extract the required information of images with image processing libraries’ implementation. 

The first thing we would need to deal with is the reconstruction of damaged or fuzzy images. While there would exist images with partial pixel losses, too much noise, or the cover of incomplete traffic signs in the image, we can have multiple functions to fix the image and proceed with valid image segmentation. Those functions include noise reduction with OpenCV, sampling, and interpolation with the combination of multiple images taken in the same milliseconds. We would also have to deal with most of the images that serve different traffic signs from different angles and perspectives. In this case, the morphological operations in OpenCV help determine the current image’s angles and rebuild those traffic signs into regular front-facing shapes. 


Image segmentation is used to separate traffic signs and the background components in an image. This can be achieved with the two main processes: shape recognition and color recognition. Shape recognition requires edge and corner recognition built-in OpenCV. Since all traffic signs stay a formal shape in geometry, traffic signs can be distinctly recognized under formal shapes. Also, segmentation under color recognition is essential, while different signs can be classified as signs with different colors. 

The second challenge that we would face is the recognition of sign patterns. Since traffic signs may contain symbols or texts or both in the same sign, we would need to introduce further functions to recognize text. Symbols recognition is planned to be done with sample template matching while we need to insert a large set of traffic signs images as a database. And this can be found in: 
https://www.kaggle.com/stavanjoshi/road-signs-in-canada


## Goals and Deliverables
Since this project aims for the accuracy of traffic sign recognition, the system’s main goal should be able to “read” the traffic signs in the images and reflect functionalities. These include being able to recognize the existence of traffic signs, separate traffic signs from the background, and comprehend the traffic signs instructions. The recognition includes classifying types of traffic signs, extracting traffic signs patterns, and translating the signs into driving constructions to human beings and the driving assistance AI. 

While the above are basic expectations, further, some advanced functions can be added to the system. The system would also track the traffic signs’ location based on the relative location of the camera, which includes distance, direction, and time expected to pass the signs. Also, the system’s processing speed is out of the project’s main goal but preferred for advanced achievement. 


The final result presents the original image and the traffic signs in the images with the corresponding instructions. The validation can only be approved by human beings with the result from the system and the meanings of signs from human visions. A successful recognition also includes the catch and prompt of recognition errors under damaged images and special cases. Finally, an statistical analysis of successful proceedings should be presented with successful rate, bias, and proceeding time spent. 

It is credible to finish the image processing part, which separates the traffic signs from the background, constructs the formal shape with morphological operations, and classifies the signs based on shape recognition and color recognition. The definition part of traffic signs patterns is challenging and is expected to take more time than the project time given. 

## Schedule

Feb 6 - Feb 13	Get familiar with OpenCV and Python.

Feb13 - Feb 20	Image Acquisition and find Canada traffic sign image database

Feb 20 - Feb 27	image processing (noise reduction, fuzzy image, etc.)

Feb 27 - March 6	image processing (image color and shape: brightness, shadow, etc.）

March 6 - March 13	Analysis of Algorithms for image recognition

March 13 - March 20	image recognition (Image matching, information extraction）

March 20 - March 27	image recognition (Image matching, information extraction）

March 27 - April 3	image recognition (Image matching, information extraction）

April 3 - April 10	error analysis (finding bugs)

April 10 - April 14	Final perfection and inspection of project



## Code

## match.py
Main program for the project
 - Read dataset images
 - Proceed color masks
 - Proceed contour segmentation and cropping
 - Proceed feature matching with dataset
 - **Provide top possible matches from each color mask**

### Usage
Run
```
python match.py
```
Default input folder ```Input```. Default dataset folder ```43 ROAD SIGNS```. 
There are some images for you to test in the Input folder.     
If you would like to change your input folder name, run
```
python match.py "input_folder"
```
or dataset folder as well
```
python match.py "input_folder" "dataset_folder"
```

## segment.py
Segment the image based on colors.     
Supported color for road signs: ```Red``` ```Yellow``` ```Blue```
    
```python
def colorRedSegment(input, color,  threshold=5)
```
```input``` image to recognize sign. 
```color``` selected color for mask. 
```threshold``` morphology threshold. 
```return image masked by color```
  


### Usage
Run
```
python segment.py "your_image"
```
Returns the image with all color masks supported. If you want to segment by single color, run
```
python segment.py "your_image" "color_name"
```
Returns the image with the selected color mask. Support ```Red``` ```Yellow``` ```Blue```
    
![Alt text](demo/segment.png?raw=true "Segmented by all colors")

## contour.py
Find the contour from the color mask and crop the image to the contour. Used to locate final road sign position in the image. 
    
```
def cropContour(input, mask, blur=2, cannyMin=160, cannyMax=255, dilate=2, area=30)
```
```input``` Input image to crop. ```mask``` Color mask image from segment.py. ```blur``` Guassian blur matrix size. ```cannyMin``` Minimum threshold for Canny Edges. ```cannyMax``` Maximum threshold for Canny Edges. ```dilate``` Dilate matrix size. ```area``` Threshold for minimum area size of contours. ```returns cropped image by selected contours```
    
### Usage
Run
```
python contour.py "your_image"
```
It will show up all images set by the parameters and a control pannel for user to change the thresholds:    
    
![Alt text](demo/contour_image.png?raw=true "Contour")
![Alt text](demo/contour_trackbar.png?raw=true "Contour Trackbar")

## sift.py
```python
def siftMatch(input, sign, threshold=0.75)
```
```input``` Image to recognize sign. 
```sign``` Sign image from the dataset. 
```threshold``` Matching distance. 
```return number of effective match points```
    
Compare similarity between the input and the sign using SIFT as the desciptor. 



