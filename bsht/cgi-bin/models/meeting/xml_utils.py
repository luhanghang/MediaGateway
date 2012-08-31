#coding=utf-8

from lxml import *

def remove_ignorable_whitespace(root):
	for el in root.iter():
		if len(el) and el.text and not el.text.strip():
			el.text = None
		if el.tail and not el.tail.strip():
			el.tail = None

