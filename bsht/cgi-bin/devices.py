#coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect

import cgi_global
from gateway import *
from device import *
from lxml import etree


def save(request):
	encoder = Encoder()
	info = request.POST
	id = info['id']
	result = {}

	if id == '':
		xml = encoder.add(info)
		xml = etree.tostring(xml, encoding='UTF-8', xml_declaration=False, pretty_print=True)
		return HttpResponse(xml,mimetype='text/xml')
	else:
		encoder.update(info)
		return HttpResponse('<OK/>',mimetype='text/xml')

def save_spot(request):
	encoder = Encoder()
	info = request.POST
	id = info['id']
	result = {}

	if id == '':
		xml = encoder.add_spot(info)
		xml = etree.tostring(xml, encoding='UTF-8', xml_declaration=False, pretty_print=True)
		return HttpResponse(xml,mimetype='text/xml')
	else:
		encoder.update_spot(info)
		return HttpResponse('<OK/>')

def remove(request):
	encoder = Encoder()
	id = request.POST['id']
	encoder.remove(id)
	#v = Venue()
	#v.remove_encoder_by_ids(ids)
	return HttpResponse('ok')

def remove_spot(request):
	encoder = Encoder()
	id = request.POST['id']
	encoder.remove_spot(id)
	return HttpResponse('ok')

def import_spots(request):
       	xml = request.POST['src_xml']
        ids = request.POST.getlist('ids')
        id = request.POST['id']
        
        encoder = Encoder()
        xml = etree.tostring(encoder.import_spots(id,xml,ids), encoding='UTF-8', xml_declaration=False, pretty_print=True)
        return HttpResponse(xml,mimetype='text/xml')
