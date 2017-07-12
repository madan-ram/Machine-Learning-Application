import re
import nltk
import operator
import math

ignore_words=['able', 'about', 'above', 'abst', 'accordance', 'according', 'accordingly', 'across', 'act', 'actually', 'added', 'adj', 'affected', 'affecting', 'affects', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'among', 'amongst', 'and', 'announce', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apparently', 'approximately', 'are', 'aren', 'arent', 'arise', 'around', 'aside', 'ask', 'asking', 'auth', 'available', 'away', 'awfully', 'back', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'beginnings', 'begins', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond', 'biol', 'both', 'brief', 'briefly', 'but', 'came', 'can', 'cannot', "can't", 'cause', 'causes', 'certain', 'certainly', 'com', 'come', 'comes', 'contain', 'containing', 'contains', 'could', 'couldnt', 'date', 'did', "didn't", 'different', 'does', "doesn't", 'doing', 'done', "don't", 'down', 'downwards', 'due', 'during', 'each', 'edu', 'effect', 'eight', 'eighty', 'either', 'else', 'elsewhere', 'end', 'ending', 'enough', 'especially', 'et-al', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'except', 'far', 'few', 'fifth', 'first', 'five', 'fix', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'found', 'four', 'from', 'further', 'furthermore', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'goes', 'gone', 'got', 'gotten', 'had', 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'hed', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'heres', 'hereupon', 'hers', 'herself', 'hes', 'hid', 'him', 'himself', 'his', 'hither', 'home', 'how', 'howbeit', 'however', 'hundred', "i'll", 'immediate', 'immediately', 'importance', 'important', 'inc', 'indeed', 'index', 'information', 'instead', 'into', 'invention', 'inward', "isn't", 'itd', "it'll", 'its', 'itself', "i've", 'just', 'keep', 'keeps', 'kept', 'know', 'known', 'knows', 'largely', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', 'lets', 'like', 'liked', 'likely', 'line', 'little', "'ll", 'look', 'looking', 'looks', 'ltd', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'might', 'million', 'miss', 'more', 'moreover', 'most', 'mostly', 'mrs', 'much', 'mug', 'must', 'myself', 'name', 'namely', 'nay', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'ninety', 'nobody', 'non', 'none', 'nonetheless', 'noone', 'nor', 'normally', 'nos', 'not', 'noted', 'nothing', 'now', 'nowhere', 'obtain', 'obtained', 'obviously', 'off', 'often', 'okay', 'old', 'omitted', 'once', 'one', 'ones', 'only', 'onto', 'ord', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'owing', 'own', 'page', 'pages', 'part', 'particular', 'particularly', 'past', 'per', 'perhaps', 'placed', 'please', 'plus', 'poorly', 'possible', 'possibly', 'potentially', 'predominantly', 'present', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'put', 'que', 'quickly', 'quite', 'ran', 'rather', 'readily', 'really', 'recent', 'recently', 'ref', 'refs', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'respectively', 'resulted', 'resulting', 'results', 'right', 'run', 'said', 'same', 'saw', 'say', 'saying', 'says', 'sec', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sent', 'seven', 'several', 'shall', 'she', 'shed', "she'll", 'shes', 'should', "shouldn't", 'show', 'showed', 'shown', 'showns', 'shows', 'significant', 'significantly', 'similar', 'similarly', 'since', 'six', 'slightly', 'some', 'somebody', 'somehow', 'someone', 'somethan', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specifically', 'specified', 'specify', 'specifying', 'still', 'stop', 'strongly', 'sub', 'substantially', 'successfully', 'such', 'sufficiently', 'suggest', 'sup', 'sure', 'take', 'taken', 'taking', 'tell', 'tends', 'than', 'thank', 'thanks', 'thanx', 'that', "that'll", 'thats', "that've", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'thered', 'therefore', 'therein', "there'll", 'thereof', 'therere', 'theres', 'thereto', 'thereupon', "there've", 'these', 'they', 'theyd', "they'll", 'theyre', "they've", 'think', 'this', 'those', 'thou', 'though', 'thoughh', 'thousand', 'throug', 'through', 'throughout', 'thru', 'thus', 'til', 'tip', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'twice', 'two', 'under', 'unfortunately', 'unless', 'unlike', 'unlikely', 'until', 'unto', 'upon', 'ups', 'use', 'used', 'useful', 'usefully', 'usefulness', 'uses', 'using', 'usually', 'value', 'various', "'ve", 'very', 'via', 'viz', 'vol', 'vols', 'want', 'wants', 'was', "wasn't", 'way', 'wed', 'welcome', "we'll", 'went', 'were', "weren't", "we've", 'what', 'whatever', "what'll", 'whats', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'wheres', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whim', 'whither', 'who', 'whod', 'whoever', 'whole', "who'll", 'whom', 'whomever', 'whos', 'whose', 'why', 'widely', 'willing', 'wish', 'with', 'within', 'without', "won't", 'words', 'world', 'would', "wouldn't", 'www', 'yes', 'yet', 'you', 'youd', "you'll", 'your', 'youre', 'yours', 'yourself', 'yourselves', "you've", 'zero']

def tokenizer(string):
	return re.sub("[^\w]"," ",string).split()

def stopWords(stringList):
	newStringList=[]
	for i in xrange(len(stringList)):
		w=str.lower(stringList[i])
		if w not in ignore_words and len(w)>=3:
			newStringList.append(w)
	del stringList
	return newStringList

def stemWord(stringList):
	for i in xrange(len(stringList)):
		w=stringList[i]
		stringList[i]=nltk.stem.lancaster.LancasterStemmer().stem(w)

def indexer(dataAllList,numberOfDoc):
	term_and_docId_list=[]
	index=[]
	prevIteam=""
	prevId=-1
	for i in xrange(len(dataAllList)):
		l=dataAllList[i]
		for w in l:
			term_and_docId_list.append([w,i])
	(term_and_docId_list).sort(key=operator.itemgetter(0))
	for d in term_and_docId_list:
		iteam=d[0]
		docId=d[1]
		if iteam==prevIteam and prevId==docId:
			pos=len(index)-1
			index[pos][len(index[pos])-1][1]+=1
		elif iteam==prevIteam and prevId!=docId:
			pos=len(index)-1
			index[pos][1]+=1
			(index[pos]).append([docId,1])
		elif iteam!=prevIteam:
			index.append([iteam,1,[docId,1]])
		prevIteam=iteam
		prevId=docId
	iteamWithPos={}
	for i in xrange(len(index)):
		index[i][1]=numberOfDoc/float(index[i][1])
		iteamWithPos[index[i][0]]=i
	return index,iteamWithPos

def processData(data,disableStopWords=True):
	dataToken=[]
	for i in xrange(len(data)):
		dataToken.append(tokenizer(data[i]))

		if disableStopWords==False:
			ListOfWord=[]
			for i in xrange(len(dataToken)):
				ListOfWord.append(stopWords(dataToken[i]))
		else:
			ListOfWord=dataToken
	for i in xrange(len(ListOfWord)):
		stemWord(ListOfWord[i])
	return ListOfWord

def score(ListOfQuery,numberOfDoc,ListOfIndexDoc,iteamWithPos):
	sumScore=[]
	for i in xrange(numberOfDoc):
		sumScore.append(0.0)
	for qw in ListOfQuery:
		pos=iteamWithPos.get(qw)
		if pos!=None:
			l=ListOfIndexDoc[pos][2:]
			for docId,tf in l:
				sumScore[docId]+=(1.0+math.log(tf,10))*(ListOfIndexDoc[pos][1])
	return sumScore


def main(doc,query):
	numberOfDoc=len(doc)
	scoreList=[]
	ListOfWord=processData(doc)
	ListOfQuerys=processData(query)
	ListOfIndexDoc,iteamWithPos=indexer(ListOfWord,numberOfDoc)
	for ListOfQuery in ListOfQuerys:
		scoreList.append(score(ListOfQuery,numberOfDoc,ListOfIndexDoc,iteamWithPos))
	return scoreList


def getWords():
	setA=[]
	setB=[]
	N=input()
	for T in xrange(N):
		setA.append(raw_input())
	raw_input()
	for T in xrange(N):
		setB.append(raw_input())
	query=setA
	doc=setB
	score=main(doc,query)
	for i in score:
		p=i.index(max(i))
		print p+1

getWords()
