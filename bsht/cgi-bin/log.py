#coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect

import cgi_global
import time

def view(request):
  t = time.strftime('/var/log/smartvision/%Y-%m-%d.log',time.localtime(time.time()))
  file = open(t,"r")
  data = file.read()
  file.close()
  return HttpResponse(data) 

