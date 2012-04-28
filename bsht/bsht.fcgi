#!/usr/bin/python
import sys, os

sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))

os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
