import re
from porter import PorterStemmer

dictionaryPo={}
dictionarySo={}
dictionaryProbComPo={}
weightPo=0
weightSo=0
dictionaryProbIndPo={}
dictionaryProbIndSo={}
removeWord=[]
#read in training data lines from files, and stopwords (useless words)
f=open("training.txt");
v=open("test.txt");
dataFile = open("temp1.txt", "w")
comDataFile = open("com.txt", "w")
testFile = open("output.txt", "w")
stopWord=open("stopwords.txt").read()
stopWord=stopWord.split("\n")
stemmer= PorterStemmer()
countPo=0
countSo=0
trainingSet=f.readlines()
testingSet=v.readlines()
trainingSet=trainingSet
testingSet=testingSet

#initialize the stemmer object for (optional) stemming later
stemmer= PorterStemmer()
stopWord=stemmer.stem(stopWord,0,len(stopWord)-1)

def getCleanString(string):
        """
                fix the string for best results
		the cleaning involve 
		(
			remove all the special character except _ and - ,
			convert upper case to lower case letter
			stemmering "remove [word with]ing|s|ed...etc"
		)
        """
        string=re.sub(r'([^a-zA-Z\-\_])|(http.+)','',string)
        string=string.lower()
        string=stemmer.stem(string,0,len(string)-1)
        return string;


def trainingString(strings,label):
        """
                this is a trianing area
		where we insert word in to dictonary with there frequency
		and you can see previousString this variable hold the previous string 
		which is used in bigram(that is two word)...
        """
        global stopWord
	global countPo
	global countSo
	if label=='Politics':
		countPo=countPo+1 #countPo is used to find the total number of Politics line
	else:
		countSo=countSo+1 #countSo is used to find the total number of sports line

	previousString=""
        for string in strings:
                string=getCleanString(string)
                if string not in stopWord and string!="" and len(string)>2:
                        if(label=='Politics'):
				if previousString!="":
					dictionaryPo[previousString+" "+string]=dictionaryPo.get(previousString+" "+string,0)+1 
					#this is used to find the frequency of bigram
				dictionaryPo[string]=dictionaryPo.get(string,0)+1
				#this is used to find the frequency of unigram
				previousString=string
                        else:
				if previousString!="":
					dictionarySo[previousString+" "+string]=dictionarySo.get(previousString+" "+string,0)+1
					#this is used to find the frequency of bigram
                                dictionarySo[string]=dictionarySo.get(string,0)+1
				#this is used to find the frequency of unigram
				previousString=string                    

def computeProbablity():
        """
                compute the probablity based on the frequency and the word existing in Politic or Sport or both
		(we see dictionaryProbComPo[x]>=0.2 and dictionaryProbComPo[x]<=.98: which squashes the common or more general word)
		note that the dictionaryProbComPo is the probablity of politics only(1-dictionaryProbComPo is sports)
        """
        for x in dictionaryPo:
                if x in dictionarySo:
                        dictionaryProbComPo[x]=dictionaryPo[x]/float(dictionaryPo[x]+dictionarySo[x])
                        if dictionaryProbComPo[x]>0.2 and dictionaryProbComPo[x]<.98:
                                removeWord.append(x) #remove those word which satisfies the condition (remove general word)      
                else:
                        dictionaryProbIndPo[x]=1.0   #if the word is independent (it belong only to set polotics)

        for x in dictionarySo:
                if x not in dictionaryPo:
                        dictionaryProbIndSo[x]=1.0   #if the word is independent (it belong only to set sports)
        for x in removeWord:
                dictionaryProbComPo.pop(x, None)
                dictionaryPo.pop(x, None)
                dictionarySo.pop(x, None)



def compareString(string):
	"""
		insert weigth (1)
		remove stop word and the string.length > 2
		if word is more toward politics 
			insert weigth to politics
		else
			insert weight to sports
	"""
	global weightPo
        global weightSo
	if string not in stopWord and string!="" and len(string)>2:
		#the common word in both sports and politics then the probality of ploltic word > 0.98 is ploltic else sports 
		if string in dictionaryProbComPo:
			if(dictionaryProbComPo[string]>0.98):
				weightPo=1+weightPo
			elif(dictionaryProbComPo[string]<0.2):
				weightSo=1+weightSo
                                                
		elif string in dictionaryProbIndPo:
			weightPo=1+weightPo
 		elif string in dictionaryProbIndSo:
			weightSo=1+weightSo



def verifyModel1():
	"""
		note that this is used in training.txt see below for verifyModel2() for text.txt
		this is varification or test area
		we check for both unigram and bigram string and there weigth from compareString()
	"""
        counterr=0
        countcor=0
	global weightPo
        global weightSo
	previousString=""
        for lines in testingSet:
                line=lines.split(" ",2)
                strings=line[2]
                strings=strings[1:-2].split()
                for string in strings:
                        string=getCleanString(string)
                        compareString(string)

			if previousString!="":
				biString=previousString+" "+string	
				compareString(biString)	#compute the weigth on bigram data

			previousString=string
                        


                if weightPo > weightSo:
                        if(line[1]!='Politics'):
                                counterr=counterr+1
                                print >> dataFile,line[0],"Politics",line[1],weightPo,weightSo,line[2]
                        else:
                                countcor=countcor+1
                        
                elif weightPo < weightSo:
                        if(line[1]!='Sports'):
                                counterr=counterr+1
                                print >> dataFile,line[0],"Sports",line[1],weightPo,weightSo,line[2]
                        else:
                                countcor=countcor+1
		else:
			if countSo<countPo:
				if(line[1]!='Politics'):
                                	counterr=counterr+1
				 	print >> dataFile,line[0],"Politics",line[1],weightPo,weightSo,line[2]
			else:
				if(line[1]!='Sports'):
                                	counterr=counterr+1
					print >> dataFile,line[0],"Sports",line[1],weightPo,weightSo,line[2]
                weightPo=0
                weightSo=0
        print "the correct result is",countcor
        print "the error result is",counterr
        print "the correct prob",countcor/(float)(counterr+countcor)
                
def verifyModel2():
	"""
		this is text area(we compute the weigth on test string's)
	"""
        global weightPo
        global weightSo
	previousString=""
        for lines in testingSet:
                line=lines.split(" ",1)
                strings=line[1]
                strings=strings[1:-2].split()
                for string in strings:
                        string=getCleanString(string)
                        compareString(string)

			if previousString!="":
				biString=previousString+" "+string	
				compareString(biString) #compute the weigth on bigram data

			previousString=string
                        
                if weightPo > weightSo:
                        print >> testFile,line[0],"Politics"
                elif weightPo < weightSo:
                        print >> testFile,line[0],"Sports"
                else:
			if countSo<countPo: 
				#if we get noise then we would put the noise to max count label
				#(because the test file was only acceped when equal number of twitterid was found by your validation script)
				print >> testFile,line[0],"Politics"
			else:
				print >> testFile,line[0],"Sports"
                weightPo=0
                weightSo=0


for lines in trainingSet:
        line=lines.split(" ",2)
        strings=line[2]
        strings=strings[1:-2].split()
        
        
        if(line[1]=='Politics'):
                trainingString(strings,"Politics")
        else:
                trainingString(strings,"Sports")


computeProbablity()
#verifyModel1()
verifyModel2()
print len(dictionarySo)
print len(dictionaryPo)
f.close()
