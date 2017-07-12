from django.shortcuts import render
from authenticate.models import Client
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
import json

# Create your views here.
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
f=open("authenticate/initapp.json")
d=json.load(f)
consumer_key=d['CONSUMER_KEY']
consumer_secret=d['CONSUMER_SECRET']
client=Client(consumer_key,consumer_secret)

def register(request):
	if 'token' not in request.session.keys() or request.session['token']==None:
		t=get_template('register.html')
		url=client.get_oauth_url(REQUEST_TOKEN_URL,AUTHORIZE_URL)
		html=t.render(Context({'oauth_req_url':url}))
		return HttpResponse(html)
	else:
		return HttpResponseRedirect("../search")

def validate(request):
	verify=request.GET['PIN']
	token,secret=client.get_access_token(verify,ACCESS_TOKEN_URL)
	if token!=None:
		request.session['token']=token
		request.session['secret']=secret
		request.session['consumer_key']=consumer_key
		request.session['consumer_secret']=consumer_secret
		return HttpResponseRedirect("../search")
	else:
		request.session['token']=None
		request.session['secret']=None
		request.session['consumer_key']=None
		request.session['consumer_secret']=None
		return HttpResponseRedirect("../")