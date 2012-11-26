#coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpRequest,HttpResponse,HttpResponseNotFound, HttpResponseRedirect
from settings import BASE_DIR

import cgi_global
from spot import Spot

def get(request):
	id = request.GET["id"];
	spot = Spot()
	return HttpResponse(spot.getGis(id))