from sklearn import svm
import numpy as np
from cPickle import dump,HIGHEST_PROTOCOL,load
from sklearn.metrics import classification_report,confusion_matrix
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import shutil
import os
import sys
import cv2
import math
from BoW import getImmediateSubdirectories,getWordsInImages,getCentroids,computeHistrogram,computeHistrogramByLevel

labels=[]
feature=[]
featureFile=open("./data/train/histrogram.out")
for x in featureFile.read().split("\n"):
	fileData=x.split()
	try:
		if fileData[0] == 'valid_images':
			l = 1
		elif fileData[0] == 'invalid_images':
			l = 0
		feature.append(np.array(map(np.float64,fileData[1:])))
		labels.append(l)
	except Exception:
		pass


clf=svm.LinearSVC()

dataset = np.asarray(feature)
labels = np.asarray(labels)
clf.fit(dataset, labels)

labels=[]
feature=[]
featureFile=open("./data/valid/histrogram.out")
data=featureFile.read().split("\n")
for x in data:
	fileData=x.split()
	try:
		if fileData[0] == 'valid_images':
			l = 1
		elif fileData[0] == 'invalid_images':
			l = 0
		feature.append(np.array(map(float,fileData[1:])))
		labels.append(l)
	except Exception:
		pass

print len(data)
print len(feature), len(labels)
dataset = np.asarray(feature)
labels=np.array(labels)

predict=clf.predict(dataset)

print classification_report(labels, predict)
print "miss classified"
matrix=confusion_matrix(labels,predict)
plt.imshow(matrix)
for y in xrange(matrix.shape[0]):
	for x in xrange(matrix.shape[1]):
		plt.annotate(matrix[y][x],xy=(y,x),horizontalalignment='center',verticalalignment='center')
plt.show()
