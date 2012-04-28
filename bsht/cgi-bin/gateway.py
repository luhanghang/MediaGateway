#coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect

from lxml import etree
import cgi_global
from gateway import *
from spot import *
from device import *
from gis import *

import dictionary

def get_dictionary(request):
  xml = etree.tostring(dictionary.read(), encoding='UTF-8', xml_declaration=True, pretty_print=True)
  return HttpResponse(xml,mimetype='text/xml') 
	
def get_inf(request):
	ip = request.META['HTTP_HOST'].split(':')[0]
	return HttpResponse(inf(ip),mimetype='text/xml') 

def all(request):
  return HttpResponse(get_all(),mimetype='text/xml') 

def get_devices(request):
  inf = request.GET
  if inf.has_key('seq'):
    g = Gateway()
    g.set_seq(inf['seq'])
  ds = Encoder()
  xml = etree.tostring(ds.list(), encoding='UTF-8', xml_declaration=True, pretty_print=True)
  return HttpResponse(xml,mimetype='text/xml')

def get_remote_conf(request):
  ip = request.POST['ip'].strip().encode("ascii")
  port = request.POST['port'].strip().encode("ascii")
  from httpClient import *
  return HttpResponse(post(ip+':'+port,'/gateway/get_config',{'a':'a'}),mimetype='text/xml')
	
def get_all():
	root = etree.Element('Gateways')

	for i in range(0,4):
		g = etree.SubElement(root,'Gateway')
		info = Gateway().get_info()
		info['name'] = info['name'] + str(i)
		for key in info.keys():
			node = etree.SubElement(g, key)
			node.text = info[key]
		spots = etree.SubElement(g, 'Spots')
		spot_list = Spot().list()
		for s in spot_list:
			spot = etree.SubElement(spots, 'Spot')
			for key in s.keys():
				node = etree.SubElement(spot, key)
				node.text = s[key]

	return etree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=True)
			
def inf(ip=''):
	root = etree.Element('Gateway')

	info = Gateway().get_info(ip)
	for key in info.keys():
		node = etree.SubElement(root, key)
		node.text = info[key]

	return etree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=True)

def get_config(request):
    g = Gateway()
    xml = etree.tostring(g.gw_config, encoding='UTF-8', xml_declaration=True, pretty_print=True)
    return HttpResponse(xml,mimetype='text/xml')
    
def config(request):
	g = Gateway()
    	xml = etree.tostring(g.gw_config, encoding='UTF-8', xml_declaration=True, pretty_print=True)
    	extra = etree.tostring(g.extra, encoding='UTF-8', xml_declaration=True, pretty_print=True)
    	return HttpResponse(xml + "\n**********\n" + extra, mimetype='text/plain')

def save(request):
	inf = request.POST
	g = Gateway()
	g.update(inf)
	return HttpResponse('0')

def driver_update(request):
    inf = request.POST
    dictionary.update_driver(inf['id'], inf['field'], inf['value'])
    return HttpResponse('0')

def driver_add(request):
    inf = request.POST
    dictionary.add_driver(inf['xml'])
    return HttpResponse('0')

def dict_add(request):
    inf = request.POST
    dictionary.add_item(inf['category'], inf['xml'])
    return HttpResponse('0')

def dict_update(request):
    inf = request.POST
    dictionary.update_item(inf['category'], inf['id'], inf['value'])
    return HttpResponse('0')
    
def list_gis(request):
	return HttpResponse(etree.tostring(Gis().list(), encoding='UTF-8', xml_declaration=True, pretty_print=True))
