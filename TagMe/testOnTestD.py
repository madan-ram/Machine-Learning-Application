import os
import sys
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from BoW import getImmediateSubdirectories,getWordsInImages,getCentroids,computeHistrogram,computeHistrogramByLevel


if len(sys.argv)<3:
	print "the dataset folder with subfolder name as label, not provied"
	sys.exit(0)

if sys.argv[2][-1]=="/":
	sys.argv[2]=sys.argv[2][:len(sys.argv[2])-1]

labels=getImmediateSubdirectories(sys.argv[2])
pathToDatasetDir=[]
imgFilesPathsWithLabels={}
PRE_ALLOCATION_BUFFER=1000

print "------------------------------------------------------"
print "Generation SIFT words"
print "------------------------------------------------------"

if len(sys.argv)>5 and sys.argv[5]=="Dense":
	Dense=True
else:
	Dense=False

centroids=getCentroids()
f=open(sys.argv[2]+"/"+"histrogram.out","w")

datasetDir=sys.argv[2]+"/"+"Images"
for file in os.listdir(datasetDir):
	name=datasetDir+"/"+file
	imgFilesPathsWithLabels={}
	dictWordsImages={}
	imgFilesPathsWithLabels[name]=""
	dictWordsImages=getWordsInImages(imgFilesPathsWithLabels,disableSIFTWrite=True,Dense=Dense)
	allwordVocabularyHistrogram=computeHistrogramByLevel(centroids,dictWordsImages)#computeHistrogram(centroids,dictWordsImages)
	imgId=name.split("/")[3]
	print imgId
	d=map(str,(allwordVocabularyHistrogram[name]).tolist())
	print >>f,imgId," ".join(d)
