#coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect

import cgi_global
import routes
from lxml import etree

def list(request):
  xml = etree.parse('/etc/routes.xml')
  return HttpResponse(etree.tostring(xml, encoding='UTF-8', xml_declaration=True, pretty_print=True),mimetype='text/xml')

def save(request):
  xml = request.POST['xml']
  file = open('/etc/routes.xml','w')
  file.write(xml)
  file.close()
  routes.write()
  return HttpResponse('1')
