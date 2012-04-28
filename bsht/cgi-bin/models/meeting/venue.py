#coding=utf-8

from lxml import etree
from xml_utils import remove_ignorable_whitespace
from device import Decoder

class Venue(object):
	XML = '/srv/www/bsht/meeting_data/Venues.xml'
	MAX = 127
	ENCODERFIELDS = ['name','address']

	def __init__(self):
		self.fields = ['name']
		self.tag = 'Venue'
		self.root= etree.parse(Venue.XML).getroot()
	
	def list(self):
		root = etree.Element('Venues')
		all = etree.SubElement(root, self.tag)
		all.set('id','0')
		all.set('name',u'会场')
		all.set('isBranch','true')
		for v in self.root.findall(self.tag):
		  venue = etree.SubElement(all, self.tag)
		  venue.set('id', v.get('id'))
		  venue.set('name',v.find('name').text)
		  venue.set('isBranch','true')
		  for d in v.findall('Device'):
			device = etree.SubElement(venue, 'Device')
			device.set('id', d.get('id'))
			device.set('name', u'设备')
			device.set('isBranch','true')
			en = d.find('Encoder/name')
			if(en is not None):
				encoder = etree.SubElement(device, 'Encoder')
				encoder.set('id', en.getparent().get('id'))
				encoder.set('name', en.text)
			de = d.find('Decoder/name')	
			if(de is not None):
				decoder = etree.SubElement(device, 'Decoder')
				decoder.set('id', de.getparent().get('id'))
				decoder.set('name', de.text)
		return root
	
	def create(self,inf):
		venue = etree.SubElement(self.root, self.tag)
		id = self.gen_seq()
		venue.set('id', id)
		for f in self.fields:
		  item = etree.SubElement(venue, f)
		  item.text = inf[f]
		device = etree.SubElement(venue, 'Device')
		device.set('id','1')
		self.write()
		return id

	def update(self, inf):
		id = inf['id']
		venue = self.find(id) 
		for f in self.fields:
		  item = venue.find(f)
		  item.text = inf[f]
		self.write()
		return id
		

	def write(self):
		remove_ignorable_whitespace(self.root)
		file = open(Venue.XML,'w')
		file.write(etree.tostring(self.root, encoding='UTF-8', xml_declaration=True, pretty_print=True))
		file.close()

	def gen_seq(self):
		for i in range(1, Venue.MAX):
			if len(self.root.xpath(self.tag + "[@id='" + str(i) + "']")) == 0:
			  return str(i)

	def gen_device_seq(self,venue):
		for i in range(1, Venue.MAX):
			if len(venue.xpath("Device[@id='" + str(i) + "']")) == 0:
			  return str(i)

	def find(self, id):
		return self.root.find(self.tag + '[@id="' + id + '"]')


	def destroy(self, id):
		item = self.find(id)
		self.root.remove(item)
		self.write()

	def add_device(self, id):
		v = self.find(id)
		device = etree.SubElement(v, 'Device')
		id = self.gen_device_seq(v)
		device.set('id', id)
		self.write()
		return id

	def find_device(self,venue_id, device_id):
		v = self.find(venue_id)
		device = v.find('Device[@id="' + device_id + '"]')
		return {'venue':v,'device':device}

	def remove_device(self, id, device_id):
		result = self.find_device(id, device_id)
		v = result['venue']
		device = result['device']
		v.remove(device)
		d = v.findall('Device')
		if(len(d) == 0):
		  device = etree.SubElement(v,'Device')
		  device.set('id','1')
		self.write()

	def remove_encoder(self, id, device_id):
		device = self.find_device(id, device_id)['device']
		device.remove(device.find('Encoder'))
		self.write()

	def remove_decoder(self, id, device_id):
		device = self.find_device(id, device_id)['device']
		device.remove(device.find('Decoder'))
		self.write()

	def add_encoder(self, inf):
		fields = Venue.ENCODERFIELDS 
		device = self.find_device(inf['id'], inf['device_id'])['device']
		item = etree.SubElement(device,'Encoder')
		item.set('id',inf['encoder_id'])
		for f in fields:
			field = etree.SubElement(item, f)
			field.text = inf[f]
		self.write()
		
	def add_decoder(self, inf):
		fields = Decoder.FIELDS
		device = self.find_device(inf['id'], inf['device_id'])['device']
		item = etree.SubElement(device,'Decoder')
		item.set('id',inf['decoder_id'])
		for f in fields:
			field = etree.SubElement(item, f)
			field.text = inf[f]
		self.write()

	def update_encoder(self, id, inf):
		list = self.root.findall('Venue/Device/Encoder[@id="' + id + '"]')
		for item in list:
		  item.set('id', inf['unique_id'])
		  for f in Venue.ENCODERFIELDS:
			e = item.find(f)
			e.text = inf[f]
		self.write()

	def update_decoder(self, id, inf):
		list = self.root.findall('Venue/Device/Decoder[@id="' + id + '"]')
		for item in list:
			for f in Decoder.FIELDS:
			  d = item.find(f)
			  d.text = inf[f]
		self.write()

	def remove_encoder_by_id(self, id):
		list = self.root.findall('Venue/Device/Encoder[@id="' + id + '"]')
		for item in list:
		  device = item.getparent()
		  device.remove(item)
		
	def remove_decoder_by_id(self, id):
		list = self.root.findall('Venue/Device/Decoder[@id="' + id + '"]')
		for item in list:
		  device = item.getparent()
		  device.remove(item)

	def remove_encoder_by_ids(self, ids):
		for id in ids:
		  self.remove_encoder_by_id(id)
		self.write()

	def remove_decoder_by_ids(self, ids):
		for id in ids:
		  self.remove_decoder_by_id(id)
		self.write()
