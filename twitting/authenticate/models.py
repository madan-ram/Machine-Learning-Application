from django.db import models
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

	def get_oauth_url(self,oauth_request_token_url,authorize_url):
		"""
			this function return authentication url
		"""
		authorize_url=authorize_url+"?oauth_token="
		oauth = OAuth1(client_key=self.CONSUMER_KEY, client_secret=self.CONSUMER_SECRET)
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
		oauth = OAuth1(client_key=self.CONSUMER_KEY,
			client_secret=self.CONSUMER_SECRET,
			resource_owner_key=self.resource_owner_key,
			resource_owner_secret=self.resource_owner_secret,
			verifier=verifier)
		r = requests.post(url=access_token_url, auth=oauth)
		credentials = parse_qs(r.content)
		if "oauth_token" not in credentials.keys():
			return None,None
		token = credentials.get('oauth_token')[0]
		secret = credentials.get('oauth_token_secret')[0]
		self.token=token
		self.secret=secret
		return token,secret

# Create your models here.
