import os
import sys
import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans
import math
from cPickle import dump, HIGHEST_PROTOCOL,load
from scipy.cluster.vq import vq,kmeans
import matplotlib.pyplot as plt
from BoW import getImmediateSubdirectories,getWordsInImages,dict2numpy,computeCentroids,computeHistrogram,computeHistrogramByLevel


if len(sys.argv)<3:
	print "the dataset folder with subfolder name as label, not provied"
	sys.exit(0)

if sys.argv[2][-1]=="/":
	sys.argv[2]=sys.argv[2][:len(sys.argv[2])-1]

labels=getImmediateSubdirectories(sys.argv[2])
pathToDatasetDir=[]
imgFilesPathsWithLabels={}


print "------------------------------------------------------"
print "label are:"+str(labels)
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


arrayOfWordsImage=dict2numpy(dictWordsImages)
print "the number of words:"+str(len(arrayOfWordsImage))
print "------------------------------------------------------"
print "Generation vocabulary or visual words using clustering"
print "------------------------------------------------------"
if os.path.isfile("metadata"):
	file=open("metadata","r")
	metadata=load(file)
	if metadata["numberOfCluster"]!=int(sys.argv[4]):
		os.remove(sys.argv[2]+"/"+"CENTROID.file")

nclusters=int(sys.argv[4])
print "number of cluster="+str(nclusters)
centroids=computeCentroids(arrayOfWordsImage,nclusters)
print "------------------------------------------------------"
print "Coumputing Histrogram from centroids"
allwordVocabularyHistrogram=computeHistrogramByLevel(centroids,dictWordsImages)#computeHistrogram(centroids,dictWordsImages)
dictWordsImages={}
print "------------------------------------------------------"
print "The number of feature:"+str(allwordVocabularyHistrogram[allwordVocabularyHistrogram.keys()[0]].shape[0])
print "------------------------------------------------------"
print "write the histogram.out"
file=open(sys.argv[2]+"/"+"histrogram.out","w")
for name in allwordVocabularyHistrogram.keys():
	imgId=name.split("/")[3]
	d=map(str,(allwordVocabularyHistrogram[name]).tolist())
	print >>file,imgId," ".join(d)
print "------------------------------------------------------"

file=open("metadata","w")
metadata={}
metadata["numberOfCluster"]=nclusters
dump(metadata,file,protocol=HIGHEST_PROTOCOL)