import numpy as np
from sklearn import svm
import matplotlib.pyplot as plt

def getError(a,p):
	return np.absolute(np.sum(a-p))

def learn_curve(train,tarin_label,valid,valid_label,rangeOf=1,degree=3,kernel="rbf",plot=False):
	"""
		this algorithm print the learning curve
	"""
	trainError=[]
	validError=[]
	clf=svm.SVC(degree=degree,kernel=kernel)
	for i  in xrange(2,train.shape[0],rangeOf):
		clf.fit(train[:i],tarin_label[:i])
		predictTrain=clf.predict(train[:i])
		predictValid=clf.predict(valid)
		trainError.append(getError(tarin_label[:i],predictTrain))
		validError.append(getError(valid_label,predictValid))
	trainError=np.array(trainError)
	vaildError=np.array(validError)
	if plot==True:
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.plot(xrange(2,train.shape[0],rangeOf),trainError,"r-",label="training error")
		ax.plot(xrange(2,train.shape[0],rangeOf),validError,"g-",label="validation error")
		ax.set_xlabel("training set")
		ax.set_ylabel("error")
		ax.legend()
		plt.show()

	return (validError,trainError)
		