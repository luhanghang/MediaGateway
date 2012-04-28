from lxml import etree
from device import *

e = Encoder()
inf = {'id':'10','name':'test', 'encoder_id':'10'}
xml = e.save_spot(inf)
print etree.tostring(xml, encoding='UTF-8', xml_declaration=True, pretty_print=True)
#print etree.tostring(e.list(), encoding='UTF-8', xml_declaration=True, pretty_print=True)
