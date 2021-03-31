import sift
import os
import collections
import cv2
import numpy as np

signs_samples = []

Sign_Object = collections.namedtuple("Sign_Object", ['name', 'image'])

signs_folder = '43 ROAD SIGNS'
current_directory = os.getcwd()

signs_directory = os.path.join(current_directory, signs_folder)

if os.path.exists(signs_directory):
    for signsD in os.listdir(signs_directory):
        signsD_path = os.path.join(signs_directory, signsD)
        if(os.path.isdir(signsD_path)):

            for signF in os.listdir(signsD_path):
                signF_path = os.path.join(signsD_path, signF)
                if(os.path.splitext(signF_path)[1] == '.png'):
                    signs_samples.append(Sign_Object(signsD, cv2.imread(signF_path)))

#print(signs_samples)

test_folder = "tests"
test_directory = os.path.join(current_directory, test_folder)
if os.path.exists(test_directory):
    for t in os.listdir(test_directory):
        #print(t)
        test_path = os.path.join(test_directory, t)
        if not t.startswith('.') and os.path.isfile(test_path):
            test_img = cv2.imread(test_path)
            max_good = []
            for s in signs_samples:
                #print(s.name)
                num_good = sift.siftMatch(test_img, s.image)
                #print(num_good)
                max_good.append((s.name, num_good))

            target = sorted(max_good, key=lambda x: x[1], reverse=True)
            print(t, ": ")
            print(target[:3], "\n")
