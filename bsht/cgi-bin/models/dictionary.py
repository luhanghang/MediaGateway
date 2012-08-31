#coding=utf-8

from gateway import Gateway
from lxml import etree
from xml_utils import remove_ignorable_whitespace
from utils import *

def read():
	return etree.parse(Gateway.PATH + "dictionary.xml")	

def get_node(name):
	root = read()
	return root.find(name)

def get_device(id):
	devices = get_node('Devices')
	return devices.xpath('Device[@id="' + id + '"]')[0]

def get_device_index(name):
	devices = get_node('Devices')
	i = 0
	for device in devices.findall('Device'):
		if device.find('name').text == name:
			return i
		i += 1

def get_item_index(tag, name):
	items = get_node(tag)
	i = 0
	for item in items.findall('Item'):
		if item.get('name') == name:
			return i
		i += 1

def update_driver(id, field, value):
        device = get_device(id)
        f = device.find(field)
        f.text = value
        write(device.getroottree().getroot())

def add_driver(xml):
        device = etree.XML(xml)
        devices = get_node('Devices')
        devices.append(device)
        write(devices.getparent())

def add_item(category, xml):
        cate = get_node(category)
        cate.append(etree.XML(xml))
        write(cate.getparent())
        

def update_item(category, id, value):
        cate = get_node(category)
        item = cate.xpath('Item[@id="' + id + '"]')[0]
        item.set('name', value)
        write(cate.getparent())

def write(root):
	remove_ignorable_whitespace(root)
        file = open(Gateway.PATH + "dictionary.xml",'w')
	file.write(etree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=True))
	file.close()
	backup(Gateway.PATH + 'dictionary.xml')
