#coding=utf-8

import re
from gateway import Gateway
from lxml import etree
import netconf
import os

class Spot(object):

  OBJECT_MAX = 127

  OBJECT_PROPS = [ { 'id':'1', 'name':u'名称', 'field':'name','unique':True, 'validate':'.+','long_name':u'监控点名称' },
	  { 'id':'2', 'name': u'设备地址', 'field':'address', 'unique':True, 'validate':'^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])$'},
	  { 'id':'3','name': u'服务端口', 'field':'service_port', 'validate':'^\d+$', 'min':1,'max':65535 },
	  { 'id':'4','name': u'设备名称', 'field':'device_name' },
	  { 'id':'5','name': u'生产厂家', 'field':'vendor' },
	  { 'id':'6','name': u'设备类型', 'field':'device_type' },
	  { 'id':'7','name': u'GUID', 'field':'guid' },
	  { 'id':'8','name': u'PTZProtocal', 'field':'ptz_protocal' },
	  { 'id':'9','name': u'IO Addr', 'field':'io_addr', 'validate':'^\d+$', 'min':0, 'max':255, 'long_name':u'IO地址' },
	  { 'id':'10','name':u'音频端口', 'field':'audio_port', 'validate':'^\d+$', 'min':1, 'max':65535 },
	  { 'id':'16383', 'name': u'驱动程序名', 'field':'driver' },
	  { 'id':'','name':u'标识', 'field':'unique_id', 'unique':True, 'validate':'^\w+$'},
	  { 'id':'','name':u'在线', 'field':'online'}	 
	  ]

  MODULE125_PROPS = [ {'id':'1', 'name':u'名称', 'field':'name' },
	  { 'id':'2','name': u'编码类型', 'field':'encode_type' },
	  { 'id':'3','name': u'通道号', 'field':'channel' },
	  { 'id':'4','name': u'通讯模式', 'field':'com_method' },
	  { 'id':'5','name': u'源地址', 'field':'src_address' },
	  { 'id':'6','name': u'源端口', 'field':'src_port' },
	  { 'id':'7','name': u'协议类型', 'field':'protocal_type' },
	  { 'id':'8','name': u'码率', 'field':'encode_rate' },
	  { 'id':'9','name': u'分辨率', 'field':'resolution' }
	  ]

  MODULE126_PROPS = [ {'id':'1', 'name':u'名称', 'field':'name' },
	  { 'id':'2','name': u'编码类型', 'field':'encode_type' },
	  { 'id':'3','name': u'通道号', 'field':'channel' },
	  { 'id':'4','name': u'通讯模式', 'field':'com_method' },
	  { 'id':'5','name': u'源地址', 'field':'src_address' },
	  { 'id':'6','name': u'源端口', 'field':'src_port' },
	  { 'id':'7','name': u'协议类型', 'field':'protocal_type' },
	  { 'id':'8','name': u'码率', 'field':'encode_rate' }
	  ]

  gw_info = Gateway().get_info()

  def __init__(self):
	self.gw = Gateway()
	self.info = self.gw.get_config_root() 
	self.gw_node = self.gw.get_node()

  def short_list(self):
	module = self.gw_node.xpath("MODULE[@id='1']")[0]
	spot_list = []
	state = open('/tmp/gateway.state')
	states = state.read().split('\n')
	state.close()
	for tag in module.getchildren():
		spot_attrs = tag.getchildren()
		spot = { 'name':spot_attrs[0].text, 'global_id':spot_attrs[4].text,'video_in':spot_attrs[2].text }
		spot['id'] = re.search('(?<=sip:).*?(?=@)',spot['global_id']).group() 
		spot['global_id'] = 'sip:' + spot['id'] + '@' + self.gw.get_info()['host'] + ':' + self.gw.get_info()['port']
		spot['online'] = str((spot['id'] + '=1' in states) + 0)
		spot_list.append(spot)
	return spot_list

  def short_list1(self):
	module = self.gw_node.xpath("MODULE[@id='1']")[0]
	spot_list = []
	state = open('/tmp/gateway.state')
	states = state.read().split('\n')
	state.close()
	gis = open('/tmp/gis')
	gis_array = gis.read().split('\n')
	gis.close()
	for tag in module.getchildren():
		spot_attrs = tag.getchildren()
		spot = { 'name':spot_attrs[0].text.encode('utf-8'), 'global_id':spot_attrs[4].text }
		spot['id'] = re.search('(?<=sip:).*?(?=@)',spot['global_id']).group() 
		spot['global_id'] = 'sip:' + spot['id'] + '@' + self.gw.get_info()['host'] + ':' + self.gw.get_info()['port']
		spot['online'] = str((spot['id'] + '=1' in states) + 0)
		spot['gis'] = 0
		for gisinf in gis_array: 
			if gisinf.startswith(spot['id'] + '=') and spot['online'] == "1":
				spot['gis'] = gisinf
				spot_list.append(spot)
	return spot_list
	
#  def xml_list(self):
	#module = self.gw_node.xpath("MODULE")[0]
	#spots = etree.Element('Spots')
	#for tag in module.getchildren():
	#	spot_attrs = tag.getchildren()
	#	spot = etree.SubElement(spots, 'Spot', id=tag.get('id'))
	#	spot.set('name',spot_attrs[0].text)
	#return spots
	
  def xml_list(self):
  	list = self.short_list()
  	spots = etree.Element('Spots')
  	spots.set('gateway',self.gw_info['id'])
  	for item in list:
  		spot = etree.SubElement(spots,'Spot')
  		for key in item.keys():
  			spot.set(key, item[key])
  	return spots

  def all(self,ip=""):
  	if ip == "":
  		ip = netconf.get_ip()
  	state = open('/tmp/gateway.state')
	states = state.read().split('\n')
	state.close()
	module = self.gw_node.xpath("MODULE[@id='1']")[0]
	spots = etree.Element('Spots')
	for tag in module.getchildren():
		spot_attrs = tag.getchildren()
		spot = etree.SubElement(spots, 'Spot', id=tag.get('id'))
		spot.set('name',spot_attrs[0].text)
		gid = re.search('(?<=sip:).*?(?=@)',spot_attrs[4].text).group()
		spot.set('url',gid + '@' + ip + ':' + self.gw.get_info()['port'])
		spot.set('state',str((gid + '=1' in states) + 0))
	return spots

  def list(self):
	spot_list = self.short_list()
	for spot in spot_list:
		spot['unique_id'] = spot['id']
		seq = re.search('\d+',spot['video_in']).group()
		obj = self.info.xpath("OBJECT[@id='" + seq + "']")[0]
		spot['seq'] = seq
		for prop in obj.getchildren():
		  for p in Spot.OBJECT_PROPS:
			if prop.get('id') == p['id']:
			  spot[p['field']] = prop.text

	return spot_list

  @staticmethod
  def generate_seq(node, path):
	for	i in range(1, Spot.OBJECT_MAX):
	  if len(node.xpath(path + "[@id='" + str(i) + "']")) == 0:
		return str(i)

  @staticmethod
  def generate_url(id):
	return 'sip:' + id.strip() + '@' + Spot.gw_info['host'] + ':' + Spot.gw_info['port']

  @staticmethod
  def log_xml(node):
	return etree.tostring(node, encoding='UTF-8', pretty_print=True)

  def is_unique(self, key, value, id):
	for spot in self.list():
	  if id != spot['id'] and spot[key] == value: 
		return False
	return True;  

  def validate_props(self, props):
	messages = {}
	for key,value in props.items():
	  for p in Spot.OBJECT_PROPS:
		if  key == p['field']:
		  long_name = p['name']
		  if p.has_key('long_name'):
			long_name = p['long_name']

		  if p.has_key('validate') and not re.match(p['validate'], value.strip()): #验证未通过
			messages['error_' + key] = u'请填写正确的' + long_name
			continue	

		  if p.has_key('min') and (int(value.strip()) < p['min'] or int(value.strip()) > p['max']): #范围不符合要求
			messages['error_' + key] = u'请填写正确的' + long_name
			continue

		  if p.has_key('unique') and not self.is_unique(key, value, props['id']): #重复唯一
			messages['error_' + key] = long_name + u'重复'
			
	return messages

  def f(self):
	return self.info.xpath('OBJECT/MODULE/TAG/PROP[contains(text(),"sip:")]')


  def update(self, props):
	messages = self.validate_props(props)
	if len(messages) > 0: #有字段验证没通过	
		return {'spot':props,'messages':messages }
	
	id = props['id']
	tag = self.info.xpath('OBJECT/MODULE/TAG/PROP[contains(text(),"sip:' + id + '@")]')[0]
	tag = tag.getparent()
	object = self.find(id)['node']

	tag_props = tag.getchildren()
	object_props = object.getchildren()

	tag_props[0].text = props['name'].strip()
	tag_props[4].text = Spot.generate_url(props['unique_id'])

	for prop in object_props:
		for p in Spot.OBJECT_PROPS:
		  if p['id'] == prop.get('id') and props.has_key(p['field']):
			prop.text = props[p['field']].strip()

	self.write()
	return { 'spot':props, 'messages': { 'success': True } }

  def add(self, props):
	messages = self.validate_props(props)
	if len(messages) > 0:	#有字段验证没通过
		return {'spot':props,'messages': messages }
	
	seq = Spot.generate_seq(self.info, "OBJECT")

	module1 = self.gw_node.xpath('MODULE[@id="1"]')[0]
	tag1 = etree.SubElement(module1, "TAG", type="13", id=Spot.generate_seq(module1,"TAG"))
	p11 = etree.SubElement(tag1, "PROP", name=u"名称", id="1")
	p12 = etree.SubElement(tag1, "PROP", name=u"VideoIn", id="2")
	p13 = etree.SubElement(tag1, "PROP", name=u"AudioIn", id="3")
	p14 = etree.SubElement(tag1, "PROP", name=u"运行状态", id="4")
	p15 = etree.SubElement(tag1, "PROP", name=u"URL", id="5")
	p11.text = props['name'].strip()
	p12.text = "/DEVICE" + seq + "/VIDEO1"
	p13.text = "/DEVICE" + seq + "/AUDIO1"
	p14.text = "0"
	p15.text = Spot.generate_url(props['unique_id'])

	module2 = self.gw_node.xpath('MODULE[@id="2"]')[0]
	tag2 = etree.SubElement(module2, "TAG", type="13", id=Spot.generate_seq(module2,"TAG"))
	p21 = etree.SubElement(tag2, "PROP", name=u"名称", id="1")
	p22 = etree.SubElement(tag2, "PROP", name=u"COM输入端口", id="2")
	p23 = etree.SubElement(tag2, "PROP", name=u"状态", id="3")
	p21.text = 'COM' + seq
	p22.text = '/DEVICE' + seq + '/COM1'
	p23.text = '0'


	object = etree.Element('OBJECT',id=seq)

	for prop in Spot.OBJECT_PROPS:
		p = etree.SubElement(object, 'PROP', name=prop['name'], id=prop['id'])
		if props.has_key(prop['field']) and props[prop['field']].strip() != '':
			p.text = props[prop['field']].strip()

	module125 = etree.SubElement(object,'MODULE', id='125')
	tag125 = etree.SubElement(module125, 'TAG', type='13', id='1')

	module126 = etree.SubElement(object,'MODULE', id='126')
	tag126 = etree.SubElement(module126, 'TAG', type='13', id='1')

	module127 = etree.SubElement(object,'MODULE', id='127')
	tag127 = etree.SubElement(module127, 'TAG', type='13', id='1')


	for prop in Spot.MODULE125_PROPS:
		p = etree.SubElement(tag125, 'PROP', name=prop['name'], id=prop['id'])

	for prop in Spot.MODULE126_PROPS:
		p = etree.SubElement(tag126, 'PROP', name=prop['name'], id=prop['id'])


	self.info.getroot().append(object)	
	self.write()
	return { 'spot':props, 'messages':{ 'success': True } }

  def write(self):
	self.gw.write(self.info)

  def find(self, unique_id):
	spot = {}
	for s in self.list():
		if s['id'] == unique_id:
			spot = s
			break
	if spot == {}:
		return {'info':spot, 'node':None }
	
	object = self.info.xpath('OBJECT[@id="' + spot['seq'] + '"]')[0]
	for prop in object.getchildren():
		for p in Spot.OBJECT_PROPS:
		  if prop.get('id') == p['id']: 
			spot[p['field']] = prop.text

	return { 'info':spot, 'node':object }

  def get_gateway(self):
	return self.gw

  def remove(self, id_list):
	module1 = self.gw_node.xpath('MODULE[@id="1"]')[0]
	module2 = self.gw_node.xpath('MODULE[@id="2"]')[0]
	for id in id_list:
	  found = self.find(id)
	  self.info.getroot().remove(found['node'])
	  module1.remove(module1.xpath('TAG/PROP[contains(text(),"sip:' + id + '@")]')[0].getparent())
	  module2.remove(module2.xpath('TAG[PROP="COM' + found['info']['seq'] + '"]')[0])
	self.write() 
