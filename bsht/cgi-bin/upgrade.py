from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect

import os

from settings import BASE_DIR
import cgi_global
from httpClient import *
             
def ver(request):
	file=open('/tftpd/upgrade.conf')
	data=file.read()
	file.close()
	return HttpResponse(data)

def ping(request):
	return HttpResponse("1")

def check(request):
	server=request.POST['host']
	file=open('/tftpd/upgrade.conf')
	data=file.read()
	file.close()
	data=data.split('|')
	version=data[0].split(' ')[1]
	data=server + ' ' + version + '|' + data[1]
	file=open('/tftpd/upgrade.conf','w')
	file.write(data)
	file.close()
	inf=""
	file=open('/tftpd/upgrade.conf')
	data=file.read()
	file.close()
	server=data.split('|')[0].split(' ')[0]
	try:
		inf = post(server,'/upgrade/ver')
	except:
		return HttpResponse('0')
	return HttpResponse(inf)
	
def do(request):
	server=request.POST['host']
	os.system('tftp -g -r upgrade -l /upgrade/upgrade ' + server)
	os.system('chmod +x /upgrade/upgrade')
	os.system('/upgrade/upgrade')
	return HttpResponse(server)
