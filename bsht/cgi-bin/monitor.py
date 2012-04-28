#coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpRequest,HttpResponse,HttpResponseNotFound, HttpResponseRedirect
from settings import BASE_DIR

import cgi_global
from spot import Spot
from lxml import etree

def index(request):
	#if request.session.get('user',False):
  		spot = Spot()
  		lanIdx = request.GET.get('lan','0')
		lan = etree.parse(BASE_DIR + '/languages/' + lanIdx + '.xml')
		str_monitor = lan.find("monitor_source").get("string");
		str_single = lan.find("single").get("string");
		str_split = lan.find("split").get("string");
		str_screen = lan.find("screen").get("string");
		str_screens = lan.find("screens").get("string");
		str_exit = lan.find("exit").get("string");	
		str_devicelist = lan.find("device_list").get("string");
		str_fullscreen = lan.find("fullscreen").get("string");	
		str_down = lan.find("down_plugin").get("string");
		str_confirmexit = lan.find("confirm_exit").get("string");
		return render_to_response('monitor.html', {'lan':lanIdx,'spot_list':spot.short_list(), 'gateway':spot.get_gateway().get_info(), 'host':request.get_host().split(':')[0], 'monitor':str_monitor, 'single':str_single,'split':str_split,'screen':str_screen, 'screens':str_screens, 'exit':str_exit, 'devicelist':str_devicelist,'fullscreen':str_fullscreen, 'down':str_down, 'confirm_exit':str_confirmexit})  
  	#return HttpResponseRedirect('/')

def spots(request):
	spot = Spot()
	return render_to_response('spots.html', {'spot_list':spot.short_list(), 'gateway':spot.get_gateway().get_info(), 'host':request.get_host().split(':')[0]})
	
def dialog(request):
	spotId = request.GET.get('id','').strip().encode("ascii")
	spot = Spot()
	sp = {}
	for s in spot.short_list():
		if s['id'] == spotId:
			sp = s
	return render_to_response('dialog.html', {'spot':sp,'gateway':spot.get_gateway().get_info(), 'host':request.get_host().split(':')[0]})  
