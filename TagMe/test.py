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

for dirList in labels:
		datasetDir=sys.argv[2]+"/"+dirList
		for file in os.listdir(datasetDir):
			imgFilesPathsWithLabels[datasetDir+"/"+file]=dirList
masksPath={}


if len(sys.argv)>5 and sys.argv[5]=="Dense":
	print "Generation SIFT words"
	print "------------------------------------------------------"
	try:
		if sys.argv[6] and sys.argv[7]:
			for dirList in labels:
				masksDir=sys.argv[7]+"/"+dirList
				for file in os.listdir(masksDir):
					masksPath[sys.argv[2]+"/"+dirList+"/"+file]=masksDir+"/"+file
		dictWordsImages=getWordsInImages(imgFilesPathsWithLabels,masksPath,Dense=True)
	except IndexError:
		print "No masks avilable"
		print "------------------------------------------------------"
		dictWordsImages=getWordsInImages(imgFilesPathsWithLabels,Dense=True)
else:
	print "Generation SIFT words"
	print "------------------------------------------------------"
	try:
		if sys.argv[6] and sys.argv[7]:
			for dirList in labels:
				masksDir=sys.argv[7]+"/"+dirList
				for file in os.listdir(masksDir):
					masksPath[sys.argv[2]+"/"+dirList+"/"+file]=masksDir+"/"+file
		dictWordsImages=getWordsInImages(imgFilesPathsWithLabels,masksPath,Dense=False)
	except IndexError:
		print "No masks avilable"
		print "------------------------------------------------------"
		dictWordsImages=getWordsInImages(imgFilesPathsWithLabels,Dense=False)

print "Using trained vocabulary or visual words"
print "------------------------------------------------------"
centroids=getCentroids()
print "Coumputing Histrogram from centroids"
allwordVocabularyHistrogram=computeHistrogramByLevel(centroids,dictWordsImages)#computeHistrogram(centroids,dictWordsImages)
print "------------------------------------------------------"
print "write the histogram.out"
file=open(sys.argv[2]+"/"+"histrogram.out","w")
for name in allwordVocabularyHistrogram.keys():
	print name
	imgId=name.split("/")[2]
	d=map(str,(allwordVocabularyHistrogram[name]).tolist())
	print >>file,imgId," ".join(d)
print "------------------------------------------------------"