import requests,sys
import requests_oauthlib
from requests_oauthlib import OAuth1
from urlparse import parse_qs

class Client:
	def __init__(self,consumer_key,consumer_secret):
		"""
			this is class that perform basic api request and oauth
		"""
		self.CONSUMER_KEY = consumer_key
		self.CONSUMER_SECRET = consumer_secret
		self.token=None
		self.secret=None
		self.resource_owner_key=None
		self.resource_owner_secret=None

	def __get_oauth(self,OAUTH_TOKEN,OAUTH_TOKEN_SECRET):
		return OAuth1(self.CONSUMER_KEY,client_secret=self.CONSUMER_SECRET,resource_owner_key=OAUTH_TOKEN,resource_owner_secret=OAUTH_TOKEN_SECRET)

	def get_oauth_url(self,oauth_request_token_url,authorize_url):
		"""
			this function return authentication url
		"""
		authorize_url=authorize_url+"?oauth_token="
		oauth = OAuth1(self.CONSUMER_KEY, client_secret=self.CONSUMER_SECRET)
		r = requests.post(url=oauth_request_token_url, auth=oauth)

		credentials = parse_qs(r.content)
		self.resource_owner_key = credentials.get('oauth_token')[0]
		self.resource_owner_secret = credentials.get('oauth_token_secret')[0]
		authorize_url = authorize_url + self.resource_owner_key
		return authorize_url

	def get_access_token(self,verifier,access_token_url):
		"""
			from the authentication url you are redirected to 
			page where user authorise .Then an verification 
			code is generated that is taken as input(verifier)
		"""
		oauth = OAuth1(self.CONSUMER_KEY,
			client_secret=self.CONSUMER_SECRET,
			resource_owner_key=self.resource_owner_key,
			resource_owner_secret=self.resource_owner_secret,
			verifier=verifier)
		r = requests.post(url=access_token_url, auth=oauth)
		credentials = parse_qs(r.content)
		token = credentials.get('oauth_token')[0]
		secret = credentials.get('oauth_token_secret')[0]
		self.token=token
		self.secret=secret
		return token,secret

	def __prepareURL(self,url,param):
		"""
			this perenate resoruce uri for request
			it take url and param dict that as to passed 
			as request url
		"""
		for x in param.keys():
			url+="&"+x+"="+param[x]
		return url

	def get_search(self,param={}):
		oauth = self.__get_oauth(self.token,self.secret)
		url=self.__prepareURL("https://api.twitter.com/1.1/search/tweets.json?",param)
		r = requests.get(url,auth=oauth)
		return r.json()