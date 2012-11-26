#coding=utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect

import os

from settings import BASE_DIR
import cgi_global 

def read(request):
	return HttpResponse("12345,0123,340,2,0,3")