# -*- coding: UTF-8 -*-
from django.http import HttpResponse,Http404,HttpResponseRedirect
import datetime
from django import template
from django.template.loader import get_template
from django.template import Context, loader
from django.shortcuts import render,render_to_response
from mysite.models import *
from django import forms
from django.template import RequestContext
from django.core.mail  import  send_mail
from django.core.mail import EmailMultiAlternatives
from sklearn.neighbors import NearestNeighbors
from sklearn import cross_validation
import math
import urllib
import random

def user_CF(req):
	l = req.GET.getlist('l')
	ans = user_recommendation(l)
	return render_to_response('user_CF.html',{'error':True,'data':ans})
def item_CF(req):
	l = req.GET.getlist('l')
	ans = item_recommendation(l)
	return render_to_response('item_CF.html',{'error':True,'data':ans})

def punish(x):
	if x<3:
		return 1
	if x>3:
		return 5
	return 3

K=20
def user_recommendation(l):
	s=500*'3'
	me=set()
	for i in l:
		no=int(i.encode())
		me.add(no)
		s=s[0:(no-1)]+'5'+s[no:]
	obj=Rates.objects.filter()
	con=Contents.objects.filter().order_by('-no')
	mp=dict()
	for i in con:
		mp[str(i.no)]=str(i.id)
	v=[]
	for i in obj:
		v.append([punish(int(j.encode())) for j in i.score])
	neigh = NearestNeighbors(n_neighbors=K,algorithm='kd_tree',metric='minkowski')
	neigh.fit(v)
	near=neigh.kneighbors([int(j) for j in s],return_distance=False)[0]
	r=dict()
	for i in near:
		for j in range(len(v[i])):
			if r.get(j+1)==None:
				r[j+1]=v[i][j]
			else:
				r[j+1]+=v[i][j]
	r=list(sorted(r,key=r.__getitem__,reverse=True))
	ans=[]
	for i in r:
		if not(i in me):
			ans.append({'id':mp[str(i)],'no':i})
		if len(ans)==10:
			break
	return ans

def item_recommendation(l):
	file = urllib.urlopen('http://localhost/static/items.txt')
	l=[int(i.encode()) for i in l]
	v=[]
	me=set()
	for i in l:
		me.add(i)
	con=Contents.objects.filter().order_by('-no')
	mp_title=dict()
	mp=dict()
	for i in con:
		mp[str(i.no)]=str(i.id)
		mp_title[str(i.no)]=str(i.title)
	while True:
		line = file.readline()
		if not line:
			break
		line=line.strip()
		tmp=line.split(' ')
		v.append([int(i.encode()) for i in tmp])
	item=[{} for i in range(500)]
	for i in l:
		for j in range(500):
			if v[i-1][j]>0:
				item[j][i-1]=v[i-1][j]
	re_item=[]
	val={}
	for i in range(500):
		tmp=sorted(item[i],key=item[i].__getitem__,reverse=True)
		val[i]=0
		for j in item[i]:
			val[i]+=item[i][j]
		re_item.append(tmp[:3])
	li = sorted(val,key=val.__getitem__,reverse=True)
	re=[]
	for i in li:
		if val[i]==0:
		 	break
		if (i+1) in me:
			continue
		re.append(i)
		if len(re)==10:
			break
	ans=[]
	why=[]
	for i in range(500):
		why_title=[mp_title[str(j+1)]for j in re_item[i]]
		why_id=[mp[str(j+1)]for j in re_item[i]]
		why.append([{'id':why_id[j],'title':why_title[j]}for j in range(len(why_id))])

	for i in re:
		ans.append({'id':mp[str(i+1)],'no':i+1,'title':mp_title[str(i+1)],
			'why':why[i]})
	return ans


def preference(req,num):
	try:
		num=int(num)
	except ValueError:
		raise Http404
	if num%3==0:
		q=41
	elif num%3==1:
		q=151
	else:
		q=500
	obj=Contents.objects.filter(no__lt=q)
	num+=1
	if num==3:
		num=2
	if num==6:
		num=5
	return render_to_response('search_form.html', {'error': True,'data':{'data':obj,'tag':num}})


def homepage(req):
	msg=None
	return render_to_response('HomePage.html', {'error': True,'data':msg})


def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


def SendEmail(req):
	l = req.GET.getlist('l')
	ans=[]
	for i in l:
		con=Contents.objects.filter(no=i)[0]
		ans.append(con)
	title='shiyuan404的推荐'
	context={'error':True,'data':ans}
	sender = 'shiyuan404@126.com'
	if 'm' in req.GET and req.GET['m']:
		m = req.GET.getlist('m')
		mail_list=m
		t = loader.get_template("mailhtml.html")
		html_content = t.render(Context(context))
		msg = EmailMultiAlternatives(title, html_content, sender, mail_list)
		msg.attach_alternative(html_content, "text/html")
		msg.send()
		return render_to_response('successfully_mailed.html',{'error':True,'data':'Successfully mailed , now return to home page  ....'})
	return render_to_response('user_CF.html',{'error':True,'data':ans})
