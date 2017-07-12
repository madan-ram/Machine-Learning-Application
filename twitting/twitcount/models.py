from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from authenticate.models import Client
import requests,sys
from requests_oauthlib import OAuth1
import json
import re

# Create your models here.
class SearchText(models.Model):
	query=models.CharField(max_length=200)
	text=models.TextField()
	data=None
	def parse_json_store(self):
		countWords=0
		countTwit=0
		countLink=0
		query=self.data['search_metadata']['query']
		for d in self.data['statuses']:
			o=SearchText(query=query,text=d['text'])
			try:
				o.save()
				countWords+=len(d['text'].split())
				if re.compile(r'\shttp[s]?://[^\s]*\s').search(d['text']):
					countLink+=1
				countTwit+=1
			except Exception:
				""
		return countWords,countTwit,countLink

	def __prepareURL(self,url,param):
		"""
			this perenate resoruce uri for request
			it take url and param dict that as to passed 
			as request url
		"""
		for x in param.keys():
			url+="&"+x+"="+param[x]
		return url

	def __get_oauth(self,CONSUMER_KEY,CONSUMER_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET):
		return OAuth1(client_key=CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=OAUTH_TOKEN,resource_owner_secret=OAUTH_TOKEN_SECRET)

	def get_search(self,consumer_key,consumer_secret,token,secret,param={}):
		oauth = self.__get_oauth(consumer_key,consumer_secret,token,secret)
		url=self.__prepareURL("https://api.twitter.com/1.1/search/tweets.json?",param)
		r = requests.get(url,auth=oauth)
		self.data=r.json()
		return r.json()

class Metadata(models.Model):
	fieldName=models.CharField(max_length=200)
	fieldValue=models.CharField(max_length=50)

	def updateIntegerFiled(self,fieldName,value):
		gN,__ =Metadata.objects.get_or_create(fieldName=fieldName)
		if gN.fieldValue=='':
			gN.fieldValue=0
		gN.fieldValue=str(int(gN.fieldValue)+value)
		gN.save()
		return gN.fieldValue