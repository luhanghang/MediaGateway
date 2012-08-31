#coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect

import cgi_global
import record
from httpClient import *

def weeklies(request):
	spot = request.GET['spot_id']
	return HttpResponse(get(record.read_conf(),'/schedule_weeklies/list/' + spot), mimetype='text/xml')

def dailies(request):
	spot = request.GET['spot_id']
	return HttpResponse(get(record.read_conf(),'/schedule_dailies/list/' + spot), mimetype='text/xml')
	
def create_weekly(request):
	keys = ['start_hour','start_min','end_hour','end_min','last_time','color','enabled']
	params = {'spot':request.POST['spot'], 'days':request.POST['days'] }
	for key in keys:
		if request.POST.has_key(key):
			params['Schedule[' + key + ']'] = request.POST[key]
	return HttpResponse(post(record.read_conf(),'/schedule_weeklies/create',params), mimetype='text/xml')	

def create_daily(request):
	keys = ['schedule_date','start_hour','start_min','end_hour','end_min','last_time','color','enabled']
	params = {'spot':request.POST['spot'] }
	for key in keys:
		if request.POST.has_key(key):
			params['Schedule[' + key + ']'] = request.POST[key]
	return HttpResponse(post(record.read_conf(),'/schedule_dailies/create',params), mimetype='text/xml')	

def update_weekly(request):
	keys = ['start_hour','start_min','end_hour','end_min','last_time','color','enabled']
	params = {}
	for key in keys:
		if request.POST.has_key(key):
			params['Schedule[' + key + ']'] = request.POST[key]
	return HttpResponse(post(record.read_conf(),'/schedule_weeklies/update/' + request.GET['id'],params))	

def update_daily(request):
	keys = ['start_hour','start_min','end_hour','end_min','last_time','color','enabled']
	params = {}
	for key in keys:
		if request.POST.has_key(key):
			params['Schedule[' + key + ']'] = request.POST[key]
	return HttpResponse(post(record.read_conf(),'/schedule_dailies/update/' + request.GET['id'],params))	

def remove_weekly(request):
	return HttpResponse(get(record.read_conf(),'/schedule_weeklies/destroy/' + request.GET['id']))	
	
def remove_daily(request):
	return HttpResponse(get(record.read_conf(),'/schedule_dailies/destroy/' + request.GET['id']))	

def remove_weeklies(request):
	return HttpResponse(get(record.read_conf(),'/schedule_weeklies/destroy_all/' + request.GET['spot_id']))	

def remove_dailies(request):
	return HttpResponse(get(record.read_conf(),'/schedule_dailies/destroy_all/' + request.GET['spot_id'] + '?date=' + request.GET['date']))	

def record_files(request):
	spot = request.GET['spot']
	return HttpResponse(get(record.read_conf(),'/record_files/search/' + spot + '?from_date=' + request.GET['from_date'] + '&to_date=' + request.GET['to_date']), mimetype='text/xml')
