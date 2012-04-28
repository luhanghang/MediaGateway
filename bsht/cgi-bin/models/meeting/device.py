#coding=utf-8

from lxml import etree
from xml_utils import remove_ignorable_whitespace

class Decoder(object):
	XML = '/srv/www/bsht/meeting_data/decoders.xml'
	MAX = 127
	FIELDS = ['name','address','device_type','port']

	def __init__(self):
		self.tag = 'Decoder'
		self.fields = Decoder.FIELDS
		self.root= etree.parse(Decoder.XML).getroot()


	def write(self):
		remove_ignorable_whitespace(self.root)
		file = open(Decoder.XML,'w')
		file.write(etree.tostring(self.root, encoding='UTF-8', xml_declaration=True, pretty_print=True))
		file.close()

	def gen_seq(self):
		for i in range(1, Decoder.MAX):
			if len(self.root.xpath(self.tag + "[@id='" + str(i) + "']")) == 0:
			  return str(i)

	def create(self, inf):
		id = self.gen_seq()
		item = etree.Element(self.tag)
		item.set('id', id)
		for field in self.fields:
			f = etree.SubElement(item, field)
			f.text = inf[field]
		self.root.append(item)
		self.write()
		return id
	
	def set_data(self, item, inf):
		for field in self.fields:
			for key in inf.keys():
			  if field == key:
				f = item.find(key)
				f.text = inf[key]

	def find(self, id):
		return self.root.find(self.tag + '[@id="' + id + '"]')

	def update(self,inf):
		id = inf['id']
		item = self.find(id)
		self.set_data(item, inf)
		self.write()
		return id

	def destroy(self, ids):
		for id in ids:
		  item = self.find(id)
		  self.root.remove(item)
		self.write()
