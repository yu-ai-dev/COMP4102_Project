# COMP4102_Project

Final project for COMP4102A: Computer Vision in winter 2021.

## sift.py
```python
function siftMatch(input, sign, threshold=0.75)
input = image to recognize sign
sign = sign image from the dataset
threshold = matching distance
return number of effective match points
```
Compare similarity between the input and the sign

## segment.py
```python
function colorRedSegment(input, threshold=5)
input = image to recognize sign
threshold = morphology threshold
return segmented image
```
Segment image to the sign

## match.py
Read signs image from dataset folder, read images to recognize from test folder   
Provide top 3 possible match

