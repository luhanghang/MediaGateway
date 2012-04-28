#coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect

import cgi_global
import record

def read(request):
  return HttpResponse(record.read_conf())

def save(request):
  data = request.POST['record_server']
  file = open('/etc/record_server','w')
  file.write(data)
  file.close()
  return HttpResponse('1')
  
def test(request):
  return HttpResponse(record.test_connection())
