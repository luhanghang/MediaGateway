#coding=utf-8

import re
from lxml import etree
from utils import *

IP_PATTERN = re.compile(r'^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])$')
RC_FILE = "/etc/init.d/rcS"
HTTPD_CONF_FILE = "/etc/lighttpd.conf"
DNS_FILE = "/etc/resolv.conf"
TEMP_FILE = "/etc/netconf"
PROFILE = '/etc/profile'
TEMPLATE_POST = ".template"

ADDRESS_POS = 3
NETMASK_POS = 5
GATEWAY_POS = 4

TEMPLATE = {'address0':'IP_ADDR0','mask0':'MASK_ADDR0','gw0':'GW0','address1':'IP_ADDR1','mask1':'MASK_ADDR1', 'dns0':'DNS0', 'dns1':'DNS1'}

def is_valid_address(address):
	if IP_PATTERN.search(address) is None:
		return False
	else:
		return True

def get_ip(ip=""):
	if ip == "":
		file = open(TEMP_FILE, "r")
		lines = file.readlines()
		file.close()
		return lines[0].strip()	
	else:
		return ip

def read():
	file = open(TEMP_FILE, "r")
	lines = file.readlines()
	file.close()
	netconf = etree.Element('NetInterfaces')
	n0 = etree.SubElement(netconf, 'NetInterface', id='0')
	addr0 = etree.SubElement(n0,'address')
	addr0.text = lines[0].strip()
	mask0 = etree.SubElement(n0,'mask')
	mask0.text = lines[1].strip()
	gw0 = etree.SubElement(n0,'gateway')
	gw0.text = lines[4].strip()
	
	n1 = etree.SubElement(netconf, 'NetInterface', id='1')
	addr1 = etree.SubElement(n1,'address')
	addr1.text = lines[2].strip()
	mask1 = etree.SubElement(n1,'mask')
	mask1.text = lines[3].strip()
	
	file = open(DNS_FILE,"r")
	lines = file.readlines()
	file.close
	dns0 = etree.SubElement(n0, 'dns0')
	dns1 = etree.SubElement(n0, 'dns1')

	dns0.text = lines[0].strip().split(' ')[1]
	dns1.text = lines[1].strip().split(' ')[1]
	return netconf

		
def write(conf):
	#write_rcS(conf)
	#write_httpd_conf(conf)
	write_temp_file(conf)
	write_dns_file(conf)
	#write_profile(conf)

def write_temp_file(conf):
	data = conf['address0'] + "\n"
	data += conf['mask0'] + "\n"
	data += conf['address1'] + "\n"
	data += conf['mask1'] + "\n"
	data += conf['gw0'] + "\n"
	file = open(TEMP_FILE, "w")
	file.write(data)
	file.close()
	backup(TEMP_FILE)
			
def write_dns_file(conf):
	data = "nameserver " + conf['dns0'] + "\n"
	data += "nameserver " + conf['dns1']
	file = open(DNS_FILE, "w")
	file.write(data)
	file.close()
	backup(DNS_FILE)
			

def write_httpd_conf(conf):
	write_config(conf, HTTPD_CONF_FILE);

def write_rcS(conf):
	write_config(conf, RC_FILE);
	
def write_profile(conf):
	write_config(conf, PROFILE);

def write_config(conf, filename):
	file = open('/etc/backup.conf')
	data = file.read()
	file.close()
	data = data.split(' ')
	internal_ip = data[0]
	
	file = open(filename + TEMPLATE_POST)
	data = file.read()
	file.close()

	for key in conf.keys(): 
	 	data = re.sub(TEMPLATE[key],conf[key],data)
	
	data = re.sub('INTERNAL_ADDR',internal_ip,data)
	file = open(filename,"w")
	file.write(data)
	file.close()
	#backup(filename)
		
#os.system("reboot")
