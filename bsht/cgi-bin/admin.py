#coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect

import os

from settings import BASE_DIR
import cgi_global 
import netconf
from utils import *
from httpClient import *
import time
import string

def index(request):
  #if is_signed_in(request):
#		return HttpResponseRedirect('/netconf/')
#	else:
		return HttpResponseRedirect('/media/SmartVision.swf?' + str(time.time()))

def sign_in(request):
	account = request.POST['account'].strip()
	pw = request.POST['passwd'].strip()
	if account == 'admin':
		file = open(BASE_DIR + '/passwd','r')
		passwd = file.read().strip()
		file.close()
		if pw == passwd:
			request.session['user'] = 'admin'
			return HttpResponse("0")
	else:
		file = open(BASE_DIR + '/monitoruser', "r")
		lines = file.readlines()
		file.close()
		if account == lines[0].strip() and pw == lines[1].strip():
			request.session['user'] = 'monitor'
			return HttpResponse("1")
	return HttpResponse("2")

def sign_out(request):
	sign_off(request)
	return HttpResponse("2")
	
def monitor_sign_out(request):
	sign_off(request)
	return HttpResponseRedirect('/')

def sign_off(request):
	try:
		del request.session['user']
	except KeyError:
		pass
	
def get_monitor_user(request):
	if is_signed_in(request):	
		file = open(BASE_DIR + '/monitoruser', "r")
		lines = file.readlines()
		file.close()
		return HttpResponse(lines[0].strip() + ":" + lines[1].strip())
	return HttpResponseRedirect('/')

def set_monitor_user(request):
	if is_signed_in(request):
		data = request.POST['account'].strip()
		data += "\n"
		data += request.POST['passwd'].strip()
		file = open(BASE_DIR + '/monitoruser','w')                         
	        file.write(data)                       
		file.close()		
		backup(BASE_DIR + '/monitoruser')
		return HttpResponse("1")
	return HttpResponse(lines[0].strip() + ":" + lines[1].strip())	

def change_passwd(request):
	pw = request.POST['passwd'].strip()
	file = open(BASE_DIR + '/passwd','w')
	file.write(pw)	
	file.close()
	backup(BASE_DIR + '/passwd')
	return HttpResponse("1")

def netconf_read(request):
	if is_signed_in(request):
		return render_to_response('ip.html',{'netinfo':netconf.read()})
	return HttpResponseRedirect('/')

def netconf_save(request):
	conf = {}
	for attr in netconf.TEMPLATE.keys():
		conf[attr] = request.POST[attr].strip().encode("ascii")
	netconf.write(conf)
	return HttpResponse('OK')

def apply_setting(request):
	os.system('/sbin/rebootjxbase')
	return HttpResponse("OK")

def reboot(request):
	#if is_signed_in(request):
	if request.POST.has_key('timeout'):
		sleep(int(request.POST['timeout']))		
	os.system('reboot')
	return HttpResponse("System rebooting...")
	#return HttpResponseNotFount('404')

def is_signed_in(req):
	return req.session.get('user',False) and req.session.get('user',False) == 'admin'

def check_sign_in(req):
	user = req.session.get('user',False)
	if user:
		if user == 'admin':
			return HttpResponse("0")
		else:
			return HttpResponse("1")
	return HttpResponse("2")

def crossdomain(req):
	return render_to_response('crossdomain.xml')
    
def get_language(request):
	lan = request.GET['lan']
	file = open(BASE_DIR + '/languages/' + lan + '.xml')
	data = file.read()
	file.close()
	return HttpResponse(data,mimetype='text/xml') 	
	
def change_capacity(request):
	current = 512
	if os.path.isfile('/etc/capacity'):
		file = open('/etc/capacity', 'r')
		line = file.readline()
		file.close()	
		current = line.strip()	
	return render_to_response('change_capacity.html', {'current':current})

def save_capacity(request):
	if request.POST.has_key('capacity'):
		capacity = request.POST['capacity'].strip()
		if capacity.isdigit():
			file = open('/etc/capacity', 'w')
			file.write(str(string.atoi(capacity)))
			file.close()
	return HttpResponseRedirect('/change_capacity')