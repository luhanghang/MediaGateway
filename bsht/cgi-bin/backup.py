from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect

import os

from settings import BASE_DIR
import cgi_global
from utils import *
              
def read(request):
	ip = ""
	try:
		file = open('/etc/backup.conf')                              
		ip = file.readline()                                                    
		file.close()
	except IOError:
		pass                                                            
	return HttpResponse(ip)
	
def save(request):
	ip_remote = request.POST['ip_remote']
	file = open('/etc/backup.conf','w')
	file.write(ip_remote.strip())
	file.close()
	#update_version()
	return HttpResponse('1')
	
def do(request):
	os.system('/tftpd/override')
	return HttpResponse('1')

def ishost(request):
	file = open('/etc/backup.conf')
	bi = file.readline()
	file.close()
	file = open('/tmp/host')
	host = file.readline()
	file.close()
	if bi == '' or host.strip()== '0':
		return HttpResponse("0")
	return HttpResponse("1")
	
def switch_server(request):
	os.system('/sbin/switch_server')
	return HttpResponse("1")
