#coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect

from lxml import etree
import cgi_global
import netconf

def read(request):
  inf = etree.tostring(netconf.read(), encoding='UTF-8', xml_declaration=True, pretty_print=True)
  return HttpResponse(inf,mimetype='text/xml') 

