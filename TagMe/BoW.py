import os
import sys
import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans
import math
from cPickle import dump, HIGHEST_PROTOCOL,load
from scipy.cluster.vq import vq,kmeans
import matplotlib.pyplot as plt

PRE_ALLOCATION_BUFFER=100

def getImmediateSubdirectories(dir):
	"""
		this function return the immediate subdirectory list
		eg:
			dir
				/subdirectory1
				/subdirectory2
				.
				.
		return ['subdirectory1',subdirectory2',...]
	"""

	return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]


def getWordsInImages(imgFilesPath,useOpponent=False,disableSIFTWrite=False,Dense=False,masksPath=None,nfeatures=400):
	"""
		this function return dictonary of SIFT descriptor (simular to words in text, descriptor in image)
		they take image files path and masks path(optional)
	"""
	t=sys.argv[2]+"/"+"SIFT.file"
	if not(os.path.isfile(t)):
		dictWordsImages={}
		sift=cv2.SIFT(nfeatures=nfeatures)
		for imgFilepath in imgFilesPath.keys():
			if imgFilepath.endswith((".png",".jpeg",".JPG",".JPEG",".jpg",".PNG",".pgm",".PGM",".TIF",".TIFF", ".tif", ".tiff",)):
				img=cv2.imread(imgFilepath)
				width=img.shape[1]
				height=img.shape[0]
				imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
				#imgGray=cv2.GaussianBlur(imgGray,(5,5),0)
				if masksPath!=None:
					imgMask=cv2.imread(masksPath[imgFilepath])
					imgMaskGray=cv2.cvtColor(imgMask,cv2.COLOR_BGR2GRAY)
				else:
					imgMaskGray=None

				if useOpponent and Dense:
					print "Invalid choise use either dense or useOpponent"
					sys.exit(0)
				elif useOpponent:
					d=cv2.DescriptorExtractor_create("OpponentSIFT")
					kp= sift.detect(imgGray,imgMaskGray)
					kp,des=d.compute(img,kp)
				elif Dense:
					dense=cv2.FeatureDetector_create("Dense")
					kp=dense.detect(imgGray)
					kp,des=sift.compute(imgGray,kp)
				else:
					kp, des = sift.detectAndCompute(imgGray,imgMaskGray)

				keypoints=[]
				for k in kp:
					keypoints.append(np.array([k.pt, k.size, k.angle, k.response, k.octave,k.class_id]))
				dictWordsImages[imgFilepath]=(des,keypoints,(height,width))
		if(disableSIFTWrite==False):
			file=open(t,"w")
			dump(dictWordsImages,file,protocol=HIGHEST_PROTOCOL)
	else:
		file=open(t,"r")
		dictWordsImages=load(file)
	return dictWordsImages

def dict2numpy(dict):
	"""
		this function return array from dictonary
	"""
	nkeys = len(dict)
	array = np.zeros((nkeys * PRE_ALLOCATION_BUFFER, dict[dict.keys()[0]][0].shape[1]))
	pivot = 0
	for key in dict.keys():
		(value,keypoints,shape) = dict[key]
		nelements = value.shape[0]
		while pivot + nelements > array.shape[0]:
			padding = np.zeros_like(array)
			array = np.vstack((array, padding))
		array[pivot:pivot + nelements] = value
		pivot += nelements
	array = np.resize(array, (pivot, dict[dict.keys()[0]][0].shape[1]))
	return array

def computeCentroids(arrayOfWordsImage,k,max_iter=1000,batch_size=100):
	"""
		this function compute centroid (called visual words) using k-means algorithm
	"""
	if len(sys.argv)>2:
		t=sys.argv[2]+"/"+"CENTROID.file"
	else:
		print "need to provide second command line argument"
		sys.exit(0)

	if not(os.path.isfile(t)):
		#centroids, distortion = kmeans(arrayOfWordsImage,k) used in case of scpy
		cluster=MiniBatchKMeans(init='k-means++', n_clusters=k,max_iter=max_iter,init_size=3*k,batch_size=batch_size)
		cluster.fit(arrayOfWordsImage)
		centroids = cluster.cluster_centers_
		file=open(t,"w")
		dump(centroids,file,protocol=HIGHEST_PROTOCOL)
	else:
		file=open(t,"r")
		centroids=load(file)
	return centroids

def computeHistrogram(centroids,dictWordsImages):
	"""
		this function compute the histrogram for visual words
	"""
	allwordVocabularyHistrogram={}
	for name in dictWordsImages.keys():
		(des,keypoints,shape)=dictWordsImages[name]
		if des!=None:
			code,dist=vq(des,centroids)
			#mean=(np.sum(dist)/dist.shape[0])
			#standardDevation=math.sqrt(np.sum(np.power(dist-mean,2))/dist.shape[0])
			#maxDist=standardDevation+mean
			#code=code[dist<=maxDist]
			allwordVocabularyHistrogram[name], bin_edges = np.histogram(code,bins=xrange(centroids.shape[0] + 1),normed=True)
	return allwordVocabularyHistrogram

def getCentroids():
	"""
		this function get the centroids from training data
	"""
	centroids=None
	if len(sys.argv)>4:
		t=sys.argv[4]
	else:
		print "need to provide fourth command line argument"
		sys.exit(0)
	if not(os.path.isfile(t)):
		print "Invalid path or may not be CENTROIDS.file exist USAGE:./text -d [path to testing dataset] -c [path to centroids]"
		sys.exit(0)

	else:
		try:
			file=open(t,"r")
			centroids=load(file)
			if centroids==None:
				raise Exception
		except Exception:
				import traceback
				traceback.print_exc()
	return centroids

def computeHistrogramByLevel(centroids,dictWordsImages,level=2):
	allwordVocabularyHistrogram={}
	for name in dictWordsImages:
		(des,kp,shape)=dictWordsImages[name]
		height=shape[0]
		width=shape[1]
		widthStep=width/4.0
		heightStep=height/4.0
		descriptors=des
		histogramOfLevelTwo = np.zeros((16,centroids.shape[0]))
		if descriptors!=None:
			for i in xrange(descriptors.shape[0]):
				descriptor=descriptors[i]
				keypoints=kp[i]
				x=keypoints[0][0]
				y=keypoints[0][1]
				boundaryIndex = int(x / widthStep) + int(y / heightStep) *4
				shape = descriptor.shape[0]
				descriptor = descriptor.reshape(1,shape)
				code,dist=vq(descriptor,centroids)

				histogramOfLevelTwo[boundaryIndex][code]+=1

			# level 1, based on histograms generated on level two
			histogramOfLevelOne = np.zeros((4, centroids.shape[0]))
			histogramOfLevelOne[0] = histogramOfLevelTwo[0] + histogramOfLevelTwo[1] + histogramOfLevelTwo[4] + histogramOfLevelTwo[5]
			histogramOfLevelOne[1] = histogramOfLevelTwo[2] + histogramOfLevelTwo[3] + histogramOfLevelTwo[6] + histogramOfLevelTwo[7]
			histogramOfLevelOne[2] = histogramOfLevelTwo[8] + histogramOfLevelTwo[9] + histogramOfLevelTwo[12] + histogramOfLevelTwo[13]
			histogramOfLevelOne[3] = histogramOfLevelTwo[10] + histogramOfLevelTwo[11] + histogramOfLevelTwo[14] + histogramOfLevelTwo[15]

			# level 0
			histogramOfLevelZero = histogramOfLevelOne[0] + histogramOfLevelOne[1] + histogramOfLevelOne[2] + histogramOfLevelOne[3]

			if level == 0:
				return histogramOfLevelZero
			elif level == 1:
				tempZero = histogramOfLevelZero.flatten() * 0.5
				tempOne = histogramOfLevelOne.flatten() * 0.5
				result = np.concatenate((tempZero, tempOne))
				allwordVocabularyHistrogram[name]=result
			elif level == 2:
			
				tempZero = histogramOfLevelZero.flatten() * 0.25
				tempOne = histogramOfLevelOne.flatten() * 0.25
				tempTwo = histogramOfLevelTwo.flatten() * 0.5
				result = np.concatenate((tempZero, tempOne, tempTwo))
				allwordVocabularyHistrogram[name]=result
			
			else:
				allwordVocabularyHistrogram[name]=None

	return allwordVocabularyHistrogram