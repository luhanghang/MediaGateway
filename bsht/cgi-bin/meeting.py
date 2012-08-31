#coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect

from lxml import etree
import cgi_global
from device import Decoder
from venue import Venue
from conference import Conference


def decoder_list(request):
  d = Decoder()
  return HttpResponse(etree.tostring(d.root, encoding='UTF-8', xml_declaration=True, pretty_print=True),mimetype='text/xml') 

def decoder_save(request):
  d = Decoder()
  inf = request.POST
  if inf.has_key('id'):
	v = Venue()
	v.update_decoder(inf['id'],inf)
	return HttpResponse(d.update(inf))	
  else:
	return HttpResponse(d.create(inf))
	
def decoder_destroy(request):
  d = Decoder()
  ids = request.POST.getlist('id')
  d.destroy(ids)
  v = Venue()
  v.remove_decoder_by_ids(ids)
  return HttpResponse('ok')

def venue_list(request):
  v = Venue()
  return HttpResponse(etree.tostring(v.list(), encoding='UTF-8', xml_declaration=True, pretty_print=True),mimetype='text/xml') 

def venue_save(request):
  v = Venue()
  inf = request.POST
  if inf.has_key('id'):
	return HttpResponse(v.update(inf))
  else:
	return HttpResponse(v.create(inf))

def add_device(request):
  v = Venue()
  id = request.POST['id']
  return HttpResponse(v.add_device(id))

def remove_venue(request):
  v = Venue()
  id = request.POST['id']
  v.destroy(id)
  return HttpResponse('ok')

def remove_device(request):
  v = Venue()
  id = request.POST['id']
  device_id = request.POST['device_id']
  v.remove_device(id,device_id)
  return HttpResponse('ok')

def remove_encoder(request):
  v = Venue()
  id = request.POST['id']
  device_id = request.POST['device_id']
  v.remove_encoder(id,device_id)
  return HttpResponse('ok')

def remove_decoder(request):
  v = Venue()
  id = request.POST['id']
  device_id = request.POST['device_id']
  v.remove_decoder(id,device_id)
  return HttpResponse('ok')

def add_encoder(request):
  v = Venue()
  inf = request.POST
  v.add_encoder(inf)
  return HttpResponse('ok')

def add_decoder(request):
  v = Venue()
  inf = request.POST
  v.add_decoder(inf)
  return HttpResponse('ok')

def conference_inf(request):
  c = Conference()
  return HttpResponse(etree.tostring(c.inf(), encoding='UTF-8', xml_declaration=True, pretty_print=True),mimetype='text/xml') 

def conference_set_state(request):
  c = Conference()
  state = request.GET['state']
  c.set_state(state)
  return HttpResponse(state)

def conference_save(request):
  c = Conference()
  venues = request.POST.getlist('venue_id')
  inf = request.POST
  c.update(inf, venues)
  return HttpResponse('ok')
