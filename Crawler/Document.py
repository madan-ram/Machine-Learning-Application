import BeautifulSoup as bs
import urllib2 as url
from urllib import FancyURLopener

class MyOpener(FancyURLopener):
	version = '	Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0 FirePHP/0.7.2'

class DocumentSoup:
	CurrentLink=""
	def getDocumentSoup(self,link):
		DocumentSoup.CurrentLink=link
		myopener = MyOpener()
		rawHtml = myopener.open(link)
		return bs.BeautifulSoup(rawHtml)

#test=DocumentSoup()
#try:
#	print (test.getDocumentSoup("http://en.wikipedia.org/wiki/Wikipedia:Neutral_point_of_view")).prettify()
#except url.HTTPError,e:
#    print e.fp.read()