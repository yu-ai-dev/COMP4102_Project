import sift
import os
import collections
import cv2
import numpy as np
import sys
import contour
import shutil
import segment

dataset_folder = "43 ROAD SIGNS"
input_folder = "Input"


def getDataset(signs_folder):

    signs_samples = []
    current_directory = os.getcwd()

    signs_directory = os.path.join(current_directory, signs_folder)

    if os.path.exists(signs_directory):
        for signsD in os.listdir(signs_directory):
            signsD_path = os.path.join(signs_directory, signsD)
            if(os.path.isdir(signsD_path)):

                for signF in os.listdir(signsD_path):
                    signF_path = os.path.join(signsD_path, signF)
                    if(os.path.splitext(signF_path)[1] == '.png'):
                        signs_samples.append((signsD, cv2.imread(signF_path)))
    else:
        print("Dataset not found. ")
        exit()

    return signs_samples

#print(signs_samples)

def computeMatching(signs_samples, test_folder = "Contoured", ):
    #test_folder = "Contoured"
    current_directory = os.getcwd()
    test_directory = os.path.join(current_directory, test_folder)

    print("\nStart to proceed comparison .. ")

    if os.path.exists(test_directory):
        last_pack = ""
        pack_result = []
        for t in os.listdir(test_directory):
            #print(t)
            test_path = os.path.join(test_directory, t)
            if not t.startswith('.') and os.path.isfile(test_path):
                pack = "_".join(str(t).split("_")[:-1])
                print("Computing:", t)

                if(pack != last_pack):
                    if(last_pack != ""):
                        print("\nRead ", last_pack, ": ")
                        print([" ".join(x[0].split(" ")[1:]) for x in pack_result], "\n")
                        #print(pack_result[:][0].split(" ")[1])
                    last_pack = pack
                    pack_result = []

                test_img = cv2.imread(test_path)
                max_good = []
                for s in signs_samples:
                    #print(s.name)
                    num_good = sift.siftMatch(test_img, s[1])
                    #print(num_good)
                    max_good.append((s[0], num_good))

                target = sorted(max_good, key=lambda x: x[1], reverse=True)
                #print(t, ": ")
                #print(target[:3], "\n")
                pack_result.append(target[0])



def generateColorSegment(test_folder):
    current_directory = os.getcwd()
    segmented_folder = "ColorSegmented"
    if(os.path.exists(os.path.join(current_directory, segmented_folder))):
        shutil.rmtree(os.path.join(current_directory, segmented_folder))
        os.makedirs(os.path.join(current_directory, segmented_folder))
    else:
        os.makedirs(os.path.join(current_directory, segmented_folder))

    test_directory = os.path.join(current_directory, test_folder)

    print("\nGenerating color segment .. ")

    if os.path.exists(test_directory):
        for t in os.listdir(test_directory):
            test_path = os.path.join(test_directory, t)
            if not t.startswith('.') and os.path.isfile(test_path):
                print("Color segment: "+str(t))
                img = cv2.imread(test_path)
                color_segmented_list = segment.segment(img, "all")
                save_path = os.path.join(os.getcwd(), "ColorSegmented")
                for cs in color_segmented_list:
                    cv2.imwrite(os.path.join(save_path, os.path.splitext(t)[0]+"_"+cs[0]+".png"), cs[1][0])
                    cv2.imwrite(os.path.join(save_path, os.path.splitext(t)[0]+"_"+cs[0]+"_mask"+".png"), cs[1][1])
    else:
        print("Input folder not found. ")
        exit()

def generateContourSegment(test_folder = "ColorSegmented"):
    current_directory = os.getcwd()
    contoured_folder = "Contoured"
    if(os.path.exists(os.path.join(current_directory, contoured_folder))):
        shutil.rmtree(os.path.join(current_directory, contoured_folder))
        os.makedirs(os.path.join(current_directory, contoured_folder))
    else:
        os.makedirs(os.path.join(current_directory, contoured_folder))

    test_folder = "ColorSegmented"
    test_directory = os.path.join(current_directory, test_folder)

    print("\nGenerating contour segment .. ")

    if os.path.exists(test_directory):
        for t in os.listdir(test_directory):
            test_path = os.path.join(test_directory, t)
            if not t.startswith('.') and os.path.isfile(test_path):
                if("_mask" not in t):
                    print("Contour segment: "+str(t))
                    img = cv2.imread(test_path)
                    mask = cv2.imread(os.path.splitext(test_path)[0]+"_mask"+os.path.splitext(test_path)[1])
                    contoured_cropped = contour.cropContour(img, mask)
                    save_path = os.path.join(os.getcwd(), "Contoured")
                    cv2.imwrite(os.path.join(save_path, t), contoured_cropped)

if __name__ == "__main__":

    if(len(sys.argv) > 1):
        input_folder = sys.argv[1]
        if(len(sys.argv) > 2):
            dataset_folder = sys.argv[2]

    dataset = getDataset(dataset_folder)
    generateColorSegment(input_folder)
    generateContourSegment()
    computeMatching(dataset)
