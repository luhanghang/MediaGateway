#coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect
import os
import cgi_global
from gateway import *
from spot import *
#from venue import Venue

#def index(request):
#  spot = Spot()
#  return render_to_response('spots.html', { 'spot_list':spot.list(), 'gateway':spot.get_gateway().get_info(), 'host':request.get_host(), 'spot': {} }) 

def list(request):
  spot = Spot()
  xml = spot.xml_list()
  return HttpResponse(etree.tostring(xml, encoding='UTF-8', xml_declaration=True, pretty_print=True),mimetype='text/xml')

def states(request):
	out = ''
	if os.path.exists('/tmp/gateway.state'):                                                                        
		state = open('/tmp/gateway.state')                                                              
		states = state.read().split('\n')                     
		state.close()
		for s in states:
			if s.find('=1') >= 0:
				out += s.split('=')[0] + ','
	return HttpResponse(out)

def all(request):
  ip = request.META['HTTP_HOST']
  spot = Spot()
  xml = spot.all(ip)
  return HttpResponse(etree.tostring(xml, encoding='UTF-8', xml_declaration=True, pretty_print=True),mimetype='text/xml')

def backup(request):
	gateway = Gateway()
	gxml = etree.parse(Gateway.GATEWAYXML)
	exml = etree.parse(Gateway.EXTRAXML)
	root = etree.Element("Config");
	root.append(gxml.getroot());
	root.append(exml.getroot());
	return HttpResponse(etree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=True),mimetype='text/xml')
	
def restore(request):
	xml = request.FILES['Filedata']
	xml = etree.parse(xml)
	gateway = Gateway()
	gxml = xml.getroot().xpath("//LIBRARY")[0]
	exml = xml.getroot().xpath("//Extra")[0]
  	file = open(Gateway.GATEWAYXML,'w')
  	file.write(etree.tostring(gxml, encoding='UTF-8', xml_declaration=True, pretty_print=True))
  	file.close()
	file = open(Gateway.EXTRAXML,'w')
  	file.write(etree.tostring(exml, encoding='UTF-8', xml_declaration=True, pretty_print=True))
  	file.close()
	return HttpResponse("ok")	

#def save(request):
#	spot = Spot()
#	info = request.POST
#	id = info['id']
#	result = {}
#
#	if id == '':
#		result = spot.add(info)
#	else:
#		result = spot.update(info)
#		v = Venue()
#		s = spot.find(info['unique_id'])['info']
#		s['address'] = s['global_id']
#		v.update_encoder(id, s)
#	return render_to_response('spots/spot_edit.html', {'spot': result['spot'], 'messages':result['messages'] })

#def get_spot(request, id):
#	spot = Spot()
#	return render_to_response('spots/spot_edit.html', {'spot': spot.find(id)['info']})

#def remove(request):
#	spot = Spot()
#	ids = request.POST.getlist('spot_id')
#	spot.remove(ids)
#	v = Venue()
#	v.remove_encoder_by_ids(ids)
#	return HttpResponseRedirect('/spots')
