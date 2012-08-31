#coding=utf-8

from lxml import etree
from xml_utils import remove_ignorable_whitespace
from venue import Venue

class Conference(object):
	XML = '/srv/www/bsht/meeting_data/Conference.xml'

	def __init__(self):
		self.root= etree.parse(Conference.XML).getroot()
	

	def write(self):
		remove_ignorable_whitespace(self.root)
		file = open(Conference.XML,'w')
		file.write(etree.tostring(self.root, encoding='UTF-8', xml_declaration=True, pretty_print=True))
		file.close()
	
	def inf(self):
		v = Venue()
		for venue in self.root.findall('Venues/Venue'):
			name = etree.SubElement(venue, 'name')
			name.text = v.find(venue.get('id')).find('name').text
		all = etree.SubElement(self.root, 'AllVenues')
		for venue in v.root.findall('Venue'):
			_v = etree.SubElement(all, 'Venue')
			_v.set('id', venue.get('id'))
			name = etree.SubElement(_v, 'name')
			name.text = venue.find('name').text
			
		return self.root
	
	def set_state(self, state):
		self.root.find('state').text = state
		self.write()

	def update(self, inf, venues):
		self.root.find('name').text = inf['name']
		self.root.find('description').text = inf['description']
		users = self.root.find('Users')
		manager = users.find('User[@manager="true"]')
		user = users.find('User[@manager="false"]')
		manager.find('account').text = inf['manager_account']
		manager.find('passwd').text = inf['manager_passwd']
		user.find('account').text = inf['user_account']
		user.find('passwd').text = inf['user_passwd']
		self.root.remove(self.root.find('Venues'))
		Venues = etree.SubElement(self.root, 'Venues')
		for venue in venues:
		  v = etree.SubElement(Venues, 'Venue')
		  v.set('id', venue)
		self.write()

