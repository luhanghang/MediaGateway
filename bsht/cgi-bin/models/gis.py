#coding=utf-8

import re
from gateway import Gateway
from lxml import etree
from utils import *

class Gis(object):
	PROPS = [ { 'id':'1', 'name':u'服务器地址', 'field':'address'},
	  { 'id':'2', 'name': u'端口', 'field':'port'},
	  { 'id':'3','name': u'通信模式', 'field':'commtype'},
	  { 'id':'4','name': u'启用', 'field':'enabled' },
	  { 'id':'16383', 'name': u'驱动程序名', 'field':'driver' }
	  ]

	def __init__(self):
		self.gw = Gateway()
		self.info = self.gw.get_config_root()
		self.gw_node = self.gw.get_node() 
	
	def list(self):
		gis = etree.Element("GIS")
		module = self.gw_node.find('MODULE[@id="127"]')
		if module != None:
			tags = module.findall("TAG")
			for tag in tags:
				item = etree.SubElement('Item')
				for prop in self.PROPS:
					item.set(prop['field'],tag.find('PROP[id=' + prop['id'] + ']').text)
		return gis
		
  	def write(self):
        	self.gw.write(self.info)