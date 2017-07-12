from sklearn import svm
import numpy as np
from cPickle import dump,HIGHEST_PROTOCOL,load
from sklearn.metrics import classification_report,confusion_matrix
import matplotlib.pyplot as plt
import shutil
import os
import sys
import cv2
import math
from BoW import getImmediateSubdirectories,getWordsInImages,getCentroids,computeHistrogram,computeHistrogramByLevel

labels={}
f=open("./Train/labels.txt").read().split("\n")
for x in f:
	d=x.split()
	if d!=[]:
		labels[d[0]]=d[1]

feature=[]
featureFile=open("./Train/histrogram.out")
for x in featureFile.read().split("\n"):
	fileData=x.split()
	try:
		l=labels[fileData[0]]
		feature.append((l,np.array(map(np.float64,fileData[1:]))))
	except Exception:
		pass

c=feature[0][1].shape[0]
r=len(feature)
dataset=np.zeros((1,c))
labels=np.zeros(1)

for l,i in feature:
	dataset=np.vstack((dataset,i))
	labels=np.hstack((labels,l))
dataset=np.delete(dataset,0,0)
labels=np.delete(labels,0)


clf=svm.LinearSVC()



training=dataset
trainingLabel=labels
clf.fit(training,trainingLabel)
feature={}
featureFile=open("./Test/histrogram.out")
data=featureFile.read().split("\n")
for x in data:
	fileData=x.split()
	try:
		feature[fileData[0]]=np.array(map(float,fileData[1:]))
	except Exception:
		pass



labels=[]
c=feature[feature.keys()[0]].shape[0]
r=len(feature)
dataset=np.zeros((1,c))
for i in feature.keys():
	dataset=np.vstack((dataset,feature[i]))


dataset=np.delete(dataset,0,0)
validation=dataset

predict=clf.predict(validation)
count=0
f=open("labels.txt","w")
for x in feature.keys():
	print >> f,x,int(predict[count])
	print count
	count=count+1
