#coding=utf-8

import re
from gateway import Gateway
from lxml import etree
from dictionary import *
from utils import *

class Encoder(object):
	GW = Gateway()
	OBJECT_MAX = 65535
	PROPS = [ { 'id':'1', 'name':u'名称', 'field':'name','unique':True, 'validate':'.+','long_name':u'编码器名称' },
	  { 'id':'2', 'name': u'设备地址', 'field':'address', 'unique':True, 'validate':'^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])$'},
	  { 'id':'3','name': u'服务端口', 'field':'service_port', 'validate':'^\d+$', 'min':1,'max':65535 },
	  { 'id':'4','name': u'设备名称', 'field':'device_name' },
	  { 'id':'5','name': u'生产厂家', 'field':'vendor' },
	  { 'id':'6','name': u'设备类型', 'field':'device_type' },
	  { 'id':'7','name': u'GUID', 'field':'guid' },
	  { 'id':'8','name': u'PTZProtocal', 'field':'ptz_protocal' },
	  { 'id':'9','name': u'IO Addr', 'field':'io_addr', 'validate':'^\d+$', 'min':0, 'max':255, 'long_name':u'IO地址' },
	  { 'id':'10','name':u'音频端口', 'field':'audio_port', 'validate':'^\d+$', 'min':1, 'max':65535 },
          { 'id':'11','name':u'连接模式', 'field':'connect_type' },        
	  { 'id':'16383', 'name': u'驱动程序名', 'field':'driver' }
	  ]

	VIDEO_PROPS = [ {'id':'1', 'name':u'名称', 'field':'name', 'default':'video0' },
	  { 'id':'2','name': u'编码类型', 'field':'encode_type' },
	  { 'id':'3','name': u'通道号', 'field':'channel' },
	  { 'id':'4','name': u'通讯模式', 'field':'com_method' },
	  { 'id':'5','name': u'源地址', 'field':'src_address', 'default':GW.get_info()['host'] },
	  { 'id':'6','name': u'源端口', 'field':'src_port' },
	  { 'id':'7','name': u'协议类型', 'field':'protocal_type' },
	  { 'id':'8','name': u'码率', 'field':'encode_rate' },
	  { 'id':'9','name': u'分辨率', 'field':'resolution' }
	  ]

	AUDIO_PROPS = [ {'id':'1', 'name':u'名称', 'field':'name', 'default':'audio0' },
	  { 'id':'2','name': u'编码类型', 'field':'encode_type' },
	  { 'id':'3','name': u'通道号', 'field':'channel' },
	  { 'id':'4','name': u'通讯模式', 'field':'com_method' },
	  { 'id':'5','name': u'源地址', 'field':'src_address' },
	  { 'id':'6','name': u'源端口', 'field':'src_port' },
	  { 'id':'7','name': u'协议类型', 'field':'protocal_type' },
	  { 'id':'8','name': u'码率', 'field':'encode_rate' }
	  ]

	SPOT_PROPS = [ {'id':'1', 'name':u'名称', 'field':'name' },
	  { 'id':'5','name': u'URL', 'field':'URL' },
	  ]

	def __init__(self):
		self.gw = Gateway()
		self.info = self.gw.get_config_root() 
		self.gw_node = self.gw.get_node()
		self.gw_info = self.gw.get_info()
		self.extra = self.gw.extra
		self.rewrite = False

	def to_xml(self, encoder):
		encoder_id = encoder.get('id')
		en = etree.Element("Encoder", id=encoder_id)
		for prop in self.PROPS:
			value = encoder.xpath("PROP[@id='" + prop['id'] + "']")[0].text
			if value == None:
			  value = ''
			en.set(prop['field'], value)
		en.set('device', str(get_device_index(en.get('device_name'))))
		
		return en

	def find_alias(self, id):
		nodes = self.extra.xpath('Stream[@id="' + id + '"]')
		if len(nodes) == 0:
			return None
		return nodes[0]

	def add_alias(self, id, alias):
		if alias.strip() == '':
			return None
		stream = etree.SubElement(self.extra.getroot(), 'Stream')
		stream.set('id', id)
		stream.set('status','0')
		stream.set('code', alias)
		return stream

	def update_alias(self, id, alias):
		if alias.strip() == '':
			self.remove_alias(id)
			return
		stream = self.find_alias(id)
		if stream == None:
			stream = self.add_alias(id, alias)
		else:
			stream.set('code', alias)

	def remove_alias(self, id):
		stream = self.find_alias(id)
		if stream != None:
			stream.getparent().remove(stream)

	def spot_to_xml(self, encoder, spot):
		id = spot.get('id')
		s = etree.Element('Spot')
                url = spot.xpath('PROP[@id="5"]')[0].text
                s.set('id', id)
                s.set('name', spot.xpath('PROP[@id="1"]')[0].text)
                s.set('global_id',re.search('(?<=sip:).*?(?=@)',url).group())

                relay = spot.xpath('PROP[@id="6"]')
                if len(relay) == 0:
                        relay = etree.SubElement(spot, "PROP", id="6", name=u"转发")
                        relay.text = "false"
                        self.rewrite = True
                else:
                        relay = relay[0]

                s.set('relay', relay.text)
                
		alias = self.find_alias(id)
		if alias != None:
			s.set('alias', alias.get('code'))
		vnode = spot.xpath('PROP[@id="2"]')[0]

                g = re.compile('\d+')
                streamId = g.findall(vnode.text)[1]
                video = encoder.xpath("MODULE[@id='125']")[0].xpath('TAG[@id="' + streamId + '"]')[0]
                audio = encoder.xpath("MODULE[@id='126']")[0].xpath('TAG[@id="' + streamId + '"]')[0]

                for vp in self.VIDEO_PROPS:
                	value = video.xpath("PROP[@id='" + vp['id'] + "']")[0].text
                	if value == None:
                        	value = ''
                	s.set('v_' + vp['field'],value)

              	for ap in self.AUDIO_PROPS:
                 	value = audio.xpath("PROP[@id='" + ap['id'] + "']")[0].text
                 	if value == None:
                        	value = ''
                	s.set('a_' + ap['field'],value)
		return s
	

	def list(self):
		capacity = "512";
		if os.path.isfile('/etc/capacity'):
			file = open('/etc/capacity', 'r')
			line = file.readline()
			file.close()	
			capacity = line.strip()
		spots = self.gw_node.xpath("MODULE[@id='1']")[0]
		encoders = etree.Element("Encoders", name=u'编码器', capacity=capacity)
		for encoder in self.info.xpath("OBJECT[@id!='0']"):
			encoder_id = encoder.get('id')
			en = self.to_xml(encoder)
			encoders.append(en)
			
			for vnode in spots.xpath('TAG/PROP[contains(text(),"/DEVICE' + encoder_id + '/VIDEO")]'):
				spot = vnode.getparent()
				en.append(self.spot_to_xml(encoder, spot))
		if self.rewrite:
                       self.write()
		return encoders

  	def generate_seq(self, node, path):
        	for i in range(1, self.OBJECT_MAX):
        		if len(node.xpath(path + "[@id='" + str(i) + "']")) == 0:
                		return str(i)

  	def generate_url(self, id):
        	return 'sip:' + id.strip() + '@' + self.gw_info['host'] + ':' + self.gw_info['port']

	def generate_global_id(self, seq):
		r_id = to_bin('0', 7)
		gw_id = to_bin(self.gw_info['id'],7)
		type_id = to_bin('13', 4)
		spots = self.gw_node.xpath("MODULE[@id='1']")[0]
		spot_id = to_bin(seq, 14)
		return str(int(r_id + gw_id + type_id + spot_id, 2))

	def generate_import_global_id(self, encoderId, spotId):
		r_id = to_bin(encoderId, 7)
		mg_id = to_bin('125',7)
		type_id = to_bin('13', 4)
		spot_id = to_bin(spotId, 14)
		return str(int(r_id + mg_id + type_id + spot_id, 2))

	def add(self, props):
		seq = self.generate_seq(self.info, "OBJECT")
        	encoder = etree.Element('OBJECT',id=seq)

        	for prop in self.PROPS:
                	p = etree.SubElement(encoder, 'PROP', name=prop['name'], id=prop['id'])
                	if props.has_key(prop['field']) and props[prop['field']].strip() != '':
                        	p.text = props[prop['field']].strip()

        	self.info.getroot().append(encoder)
        	self.write()
		return self.to_xml(encoder)

	def update(self, props):
        	id = props['id']
		encoder = self.find(id)
		for prop in self.PROPS:
			for p in encoder.findall("PROP"):
				if props.has_key(prop['field']) and p.get('id') == prop['id']:
					p.text = props[prop['field']].strip()
        	self.write()

	def find(self, id):
		encoder = self.info.xpath("OBJECT[@id='" + id + "']")[0]
		return encoder

	def find_spot(self, id):
		return self.gw_node.xpath('MODULE[@id="1"]')[0].xpath('TAG[@id="' + id + '"]')[0]

	def get_spot_ids(self, spot):
		vnode = spot.xpath('PROP[@id="2"]')[0]
                g = re.compile('\d+')
                return g.findall(vnode.text)

	def write(self):
        	self.gw.write(self.info)

	def write_extra(self):
        	self.gw.write_extra()
	
	def update_spot(self, props):
		id = props['id']
		encoderId = props['encoder_id']
		spot = self.find_spot(id)
		ids = self.get_spot_ids(spot)	
		vId = ids[1]
		aId = ids[1]
		spot_name = spot.xpath('PROP[@id="1"]')[0]
		spot_name.text = props['name'].strip()
		relay = spot.xpath('PROP[@id="6"]')[0]
		if props.has_key('relay'):
                        relay.text = props['relay'].strip()
                else:
                        relay.text = '0'
		encoder = self.find(encoderId)
		videoStream = encoder.xpath('MODULE[@id="125"]')[0].xpath('TAG[@id="' + vId + '"]')[0]
		audioStream = encoder.xpath('MODULE[@id="126"]')[0].xpath('TAG[@id="' + aId + '"]')[0]
		for prop in self.VIDEO_PROPS:
			for p in videoStream.findall('PROP'):
				if props.has_key('v_' + prop['field']) and p.get('id') == prop['id']:
					p.text = props['v_' + prop['field']].strip()
		for prop in self.AUDIO_PROPS:
			for p in audioStream.findall('PROP'):
				if props.has_key('a_' + prop['field']) and p.get('id') == prop['id']:
					p.text = props['a_' + prop['field']].strip()
		self.write()
		if props.has_key('alias'):
			self.update_alias(id, props['alias'].strip())
			self.write_extra()

	def add_spot(self, props):
		encoderId = props['encoder_id']
		encoder = self.find(encoderId)
		
		videos = encoder.xpath('MODULE[@id="125"]')
		audios = encoder.xpath('MODULE[@id="126"]')
		coms = encoder.xpath('MODULE[@id="127"]')
		if len(videos) == 0:
			videos = etree.SubElement(encoder,'MODULE', id='125')
			audios = etree.SubElement(encoder,'MODULE', id='126')
			#coms = etree.SubElement(encoder,'MODULE', id='127')
		else:
			videos = videos[0]
			audios = audios[0]
		if len(coms) == 0:
			coms = etree.SubElement(encoder,'MODULE', id='127')
		else:	
			coms = coms[0]
			
		seq = self.generate_seq(videos, "TAG")
        	videoStream = etree.SubElement(videos, 'TAG', type='13', id=seq)
        	audioStream = etree.SubElement(audios, 'TAG', type='13', id=seq)
        	com = etree.SubElement(coms, 'TAG', type='13', id=seq)

        	for prop in self.VIDEO_PROPS:
                	p = etree.SubElement(videoStream, 'PROP', name=prop['name'], id=prop['id'])
			if props.has_key('v_' + prop['field']):
				p.text = props['v_' + prop['field']]
			elif prop.has_key('default'):
				p.text = prop['default']
			

        	for prop in self.AUDIO_PROPS:
                	p = etree.SubElement(audioStream, 'PROP', name=prop['name'], id=prop['id'])
			if props.has_key('a_' + prop['field']):
				p.text = props['a_' + prop['field']]
			elif prop.has_key('default'):
				p.text = prop['default']

		module1 = self.gw_node.xpath('MODULE[@id="1"]')[0]
		id = self.generate_seq(module1,"TAG")
        	spot = etree.SubElement(module1, "TAG", type="13")
		spot.set('id',id)
        	p11 = etree.SubElement(spot, "PROP", name=u"名称", id="1")
        	p12 = etree.SubElement(spot, "PROP", name=u"VideoIn", id="2")
        	p13 = etree.SubElement(spot, "PROP", name=u"AudioIn", id="3")
        	p14 = etree.SubElement(spot, "PROP", name=u"运行状态", id="4")
        	p15 = etree.SubElement(spot, "PROP", name=u"URL", id="5")
        	p16 = etree.SubElement(spot, "PROP", name=u"转发", id="6")
        	p11.text = props['name'].strip()
        	p12.text = "/DEVICE" + encoderId + "/VIDEO" + seq
        	p13.text = "/DEVICE" + encoderId + "/AUDIO" + seq
        	p14.text = "0"
        	p15.text = self.generate_url(self.generate_global_id(id))
        	if props.has_key('relay'):
                        p16.text = props['relay'].strip()
        	else:
                	p16.text = '0'

		module2 = self.gw_node.xpath('MODULE[@id="2"]')[0]
	        com = etree.SubElement(module2, "TAG", type="13", id=self.generate_seq(module2,"TAG"))
        	p21 = etree.SubElement(com, "PROP", name=u"名称", id="1")
        	p22 = etree.SubElement(com, "PROP", name=u"COM输入端口", id="2")
        	p23 = etree.SubElement(com, "PROP", name=u"状态", id="3")
        	p21.text = 'COM' + seq
        	p22.text = '/DEVICE' + encoderId + '/COM' + seq
		p23.text = '0'
		
		self.write()
		if props.has_key('alias'):
			self.add_alias(id, props['alias'].strip())
			self.write_extra()
		return self.spot_to_xml(encoder, spot)

	def remove(self, id):
		encoder = self.find(id)
		spots = self.gw_node.xpath("MODULE[@id='1']")[0]
		for vnode in spots.xpath('TAG/PROP[contains(text(),"/DEVICE' + id + '/VIDEO")]'):
			spot = vnode.getparent()
			self.remove_alias(spot.get('id'))
			spots.remove(spot)
		coms = self.gw_node.xpath("MODULE[@id='2']")[0]
		for cnode in coms.xpath('TAG/PROP[contains(text(),"/DEVICE' + id + '/COM")]'):
			com = cnode.getparent()
			coms.remove(com)
		encoder.getparent().remove(encoder)	
		self.write()
		self.write_extra()

	def remove_spot(self, id):
                spot = self.find_spot(id)
		ids = self.get_spot_ids(spot)
		
		com_module = self.gw_node.xpath('MODULE[@id="2"]')[0]
		com = com_module.xpath('TAG/PROP[text()="/DEVICE' + ids[0] + '/COM' + ids[1] + '"]')
		if len(com) == 1:
			com_module.remove(com[0].getparent())
		
		encoder = self.find(ids[0])
		vmodule = encoder.xpath('MODULE[@id="125"]')[0]
		amodule = encoder.xpath('MODULE[@id="126"]')[0]
		cmodule = encoder.xpath('MODULE[@id="127"]')
		
		vmodule.remove(vmodule.xpath('TAG[@id="' + ids[1] + '"]')[0])	
		amodule.remove(amodule.xpath('TAG[@id="' + ids[1] + '"]')[0])	
		
		if len(cmodule) > 0:
                        cmodule = cmodule[0]
                        tags = cmodule.xpath('TAG[@id="' + ids[1] + '"]')
			if len(tags) > 0:
                                cmodule.remove(tags[0])	

		spot.getparent().remove(spot)
		self.write()
		self.remove_alias(id)
		self.write_extra()

	def import_spots(self, id, xml, ids):
                encoder = self.find(id)
                i_xml = etree.fromstring(xml)
                i_gw = i_xml.xpath("/LIBRARY/OBJECT[@id='0']")[0]
                i_module = i_gw.xpath("MODULE[@id='1']")[0]
                new_spots = []
                for spot_id in ids:
                        i_spot = i_module.xpath("TAG[@id='" + spot_id + "']")[0]
                        vnode = i_spot.xpath('PROP[@id="2"]')[0]
                        urlnode = i_spot.xpath('PROP[@id="5"]')[0]
                        
                        g = re.compile('\d+')
                        i_ids = g.findall(vnode.text)
                        i_encoder = i_xml.xpath("OBJECT[@id='" + i_ids[0] + "']")[0]
                        i_video = i_encoder.xpath("MODULE[@id='125']")[0].xpath('TAG[@id="' + i_ids[1] + '"]')[0]
                        i_audio = i_encoder.xpath("MODULE[@id='126']")[0].xpath('TAG[@id="' + i_ids[1] + '"]')[0]

                        i_com = i_encoder.xpath("MODULE[@id='127']")
                        if len(i_com) > 0:
                                icom = i_com[0].xpath('TAG[@id="' + i_ids[1] + '"]')
                                if len(i_com) == 0:
                                        i_com = etree.Element("TAG")
                                        i_com.set("type","13")
                                else:
                                        i_com = i_com[0][0]
                        else:
                                i_com = etree.Element("TAG")
                                i_com.set("type","13")

                        videos = encoder.xpath('MODULE[@id="125"]')
                        audios = encoder.xpath('MODULE[@id="126"]')
                        coms = encoder.xpath('MODULE[@id="127"]')
                        if len(videos) == 0:
                                videos = etree.SubElement(encoder,'MODULE', id='125')
                                audios = etree.SubElement(encoder,'MODULE', id='126')
                                coms = etree.SubElement(encoder,'MODULE', id='127')
                        else:
                                videos = videos[0]
                                audios = audios[0]
                        if len(coms) == 0:
                                coms = etree.SubElement(encoder,'MODULE', id='127')
                        else:	
                                coms = coms[0]
			
                        seq = self.generate_seq(videos, "TAG")
                        videoStream = etree.SubElement(videos, 'TAG', type='13', id=seq)
                        audioStream = etree.SubElement(audios, 'TAG', type='13', id=seq)
                        com = etree.SubElement(coms, 'TAG', type='13', id=seq)
                        
                        for prop in i_video.getchildren():
                                videoStream.append(prop)

                        for prop in i_audio.getchildren():
                                audioStream.append(prop)

                        for prop in i_com.getchildren():
                                com.append(prop)

                        module1 = self.gw_node.xpath('MODULE[@id="1"]')[0]
                        new_spot_id = self.generate_seq(module1,"TAG")
                        spot = etree.SubElement(module1, "TAG", type="13")
                        spot.set('id',new_spot_id)
                        p11 = etree.SubElement(spot, "PROP", name=u"名称", id="1")
                        p12 = etree.SubElement(spot, "PROP", name=u"VideoIn", id="2")
                        p13 = etree.SubElement(spot, "PROP", name=u"AudioIn", id="3")
                        p14 = etree.SubElement(spot, "PROP", name=u"运行状态", id="4")
                        p15 = etree.SubElement(spot, "PROP", name=u"URL", id="5")
                        p16 = etree.SubElement(spot, "PROP", name=u"转发", id="6")
                        p11.text = i_spot.xpath('PROP[@id="1"]')[0].text
                        p12.text = "/DEVICE" + id + "/VIDEO" + seq
                        p13.text = "/DEVICE" + id + "/AUDIO" + seq
                        p14.text = "0"
                        p15.text = self.generate_url(self.generate_global_id(new_spot_id))
                        p16.text = "true"
                        
                        module2 = self.gw_node.xpath('MODULE[@id="2"]')[0]
                        com = etree.SubElement(module2, "TAG", type="13", id=self.generate_seq(module2,"TAG"))
                        p21 = etree.SubElement(com, "PROP", name=u"名称", id="1")
                        p22 = etree.SubElement(com, "PROP", name=u"COM输入端口", id="2")
                        p23 = etree.SubElement(com, "PROP", name=u"状态", id="3")
                        p21.text = 'COM' + seq
                        p22.text = '/DEVICE' + id + '/COM' + seq
                        p23.text = '0'
                        #i_global_id = self.generate_import_global_id(i_ids[0],i_ids[1])
                        i_global_id = urlnode.text.split('@')[0].split(':')[1]
                        self.add_alias(new_spot_id, i_global_id)
                        new_spots.append(spot)

                self.write()
                self.write_extra()
                        
                en = self.to_xml(encoder)
		for spot in new_spots:
			en.append(self.spot_to_xml(encoder, spot))
                                
		return en
