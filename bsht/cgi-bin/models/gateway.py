#coding=utf-8

from lxml import etree
from xml_utils import remove_ignorable_whitespace
from netconf import *
from httpClient import *
#GATEWAYXML = '/home/firebolt/work/smartvision/test/gateway.xml'

class Gateway(object):
	PATH = '/home/firebolt/work/smartvision/test/'
	GATEWAYXML = PATH + 'gateway.xml'
	EXTRAXML = PATH + 'extra.xml'
	SETTINGS = PATH + 'setting.xml'
	OBJ_PROPS = [{'id':'1','field':'name'},
		{'id':'2','field':'host'},
		{'id':'3','field':'port'},
		{'id':'4','field':'protocal'},
		{'id':'5','field':'apptype'},
		{'id':'7','field':'web_port'},
                {'id':'8','field':'relay_ip'},
                {'id':'9','field':'relay_port'},
                {'id':'10','field':'relay'},
		{'id':'16383','field':'driver'}]

	def __init__(self):
		self.gw_config = etree.parse(Gateway.GATEWAYXML)
		self.gw_node = self.gw_config.xpath("/LIBRARY/OBJECT[@id='0']")[0]
		self.extra = etree.parse(Gateway.EXTRAXML)
		self.settings = etree.parse(Gateway.SETTINGS)
	
	def get_manage_server_address(self):
		server = self.settings.find('ManageServer')
		url = server.get('url').lower()
		return url.lstrip('http://')
	
	def register(self):
		address = self.get_manage_server_address()
		seq = post(address, '/gateway/register', self.get_info())				
		if seq == None:
			return False
		return True

	def set_seq(self, seq):
                g = self.settings.find("Gateway")
		old_seq = g.get('id')
		if seq != old_seq:
			g.set('id', seq)
			self.write_settings()

	def get_config_root(self):
		return self.gw_config

	def get_info(self, ip=''):
		object = self.get_node()
		g = self.settings.find("Gateway")
		info = { 'id':g.get('id'),'host':get_ip(ip), 'port':object[2].text, 'web_port':object[6].text }
		info['name'] = object.xpath("PROP[@id='1']")[0].text
		info['address'] = get_ip(ip)
		info['protocal'] = object.xpath("PROP[@id='4']")[0].text
		info['apptype'] = object.xpath("PROP[@id='5']")[0].text
		info['server'] = object.xpath("PROP[@id='6']")[0].text
		info['driver'] = object.xpath("PROP[@id='16383']")[0].text
		relay_ip = object.xpath("PROP[@id='8']")
		if len(relay_ip) == 1:
                      info['relay_ip'] = relay_ip[0].text
                relay_port = object.xpath("PROP[@id='9']")
		if len(relay_port) == 1:
                      info['relay_port'] = relay_port[0].text
                relay = object.xpath("PROP[@id='10']")
		if len(relay) == 1:
                      info['relay'] = relay[0].text
                else:
                        info['relay'] = "0"
		mserver = self.settings.find('ManageServer')
		info['use_manage_server'] = mserver.get('use')
		info['manage_server_url'] = mserver.get('url')
		return info
	
	def get_node(self):
		return self.gw_node 

	def update(self, inf):
                gw = self.get_node()
                relay_ip = gw.xpath("PROP[@id='8']")
                relay_port = gw.xpath("PROP[@id='9']")
                relay = gw.xpath("PROP[@id='10']")             
                if len(relay_ip) == 0:
                        relay_ip = etree.SubElement(gw, "PROP", id="8", name=u"转发地址")     
                if len(relay_port) == 0:
                        relay_port = etree.SubElement(gw, "PROP", id="9", name=u"转发端口")
                if len(relay) == 0:
                        relay = etree.SubElement(gw, "PROP", id="10", name=u"是否转发")        
		nodes = gw.findall('PROP')
		
		for node in nodes:
		  for p in Gateway.OBJ_PROPS:
			if node.get('id') == p['id'] and inf.has_key(p['field']):
			  node.text = inf[p['field']].strip()
		self.write(self.get_config_root())
		if inf.has_key('use_manage_server'):
			ms = self.settings.find('ManageServer');
            		ms.set('use', inf['use_manage_server'])
            		ms.set('url', inf['manage_server_url'].lower().strip())
            		self.write_settings()
			if ms.get('use') == '1':	
				self.register()

	def write(self, root):
		#os.system('cp ' + Gateway.GATEWAYXML + ' ' + Gateway.GATEWAYXML + ".backup")
		remove_ignorable_whitespace(root)
		file = open(Gateway.GATEWAYXML,'w')
		file.write(etree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=True))
		file.close()
		self.gw_config = root
		backup(Gateway.PATH + 'gateway.xml')
	
	def write_extra(self):
		#os.system('cp ' + Gateway.EXTRAXML + ' ' + Gateway.EXTRAXML + ".backup")
		remove_ignorable_whitespace(self.extra)
		file = open(Gateway.EXTRAXML,'w')
		file.write(etree.tostring(self.extra, encoding='UTF-8', xml_declaration=True, pretty_print=True))
		file.close()
		backup(Gateway.PATH + 'extra.xml')
	
	def write_settings(self):
		#os.system('cp ' + Gateway.SETTINGS + ' ' + Gateway.SETTINGS + ".backup")
		remove_ignorable_whitespace(self.extra)
		file = open(Gateway.SETTINGS,'w')
		file.write(etree.tostring(self.settings, encoding='UTF-8', xml_declaration=True, pretty_print=True))
		file.close()
		backup(Gateway.PATH + 'setting.xml')
