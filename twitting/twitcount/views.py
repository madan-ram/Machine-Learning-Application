from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from twitcount.models import SearchText,Metadata
import json


ser=SearchText()
meta=Metadata()

def search(request):
	if 'q' in request.GET.keys():
		param=request.GET
		token,secret=request.session['token'],request.session['secret']
		consumer_key,consumer_secret=request.session['consumer_key'],request.session['consumer_secret']
		result=ser.get_search(consumer_key,consumer_secret,token,secret,param=param)
		numWords,numTwits,numInDb=None,None,None
		numWords,numTwits,numLink=ser.parse_json_store()
		numInDb=SearchText.objects.all().count()
		t=get_template("search.html")
		total_numb_words=meta.updateIntegerFiled("total_number_of_words",numWords)
		html=t.render(Context({'numWords':numWords,'numTwits':numTwits,'numInDb':numInDb,'total_numb_words':total_numb_words,'numLink':numLink}))
	else:
		t=get_template("search.html")
		html=t.render(Context({}))
	return HttpResponse(html)