from lxml import etree
from mask import *
from utils import *

def write():
	xml = etree.parse('/etc/routes.xml')
	data = '#!/bin/sh\n'
	for route in xml.findall('route'):
		net = route.find('net').text
		mask = from_ip(route.find('mask').text)
		gateway = route.find('gateway').text
		device = route.find('device').text
		data+="ip route add " + net + "/" + str(mask) + " via " + gateway + " dev " + device + "\n"

	file = open('/etc/addroutes','w')
	file.write(data)
	file.close()
	backup('/etc/addroutes')
	backup('/etc/routes.xml')
