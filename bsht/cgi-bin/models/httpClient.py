#-*-coding:utf-8-*-

import httplib,urllib,socket

def post(address, uri, inf={'a':'a'}):
	params = urllib.urlencode(dict([k, v.encode('utf-8')] for k, v in inf.items()))
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	try:
		conn = httplib.HTTPConnection(address,timeout=3)
		conn.request("POST", uri, params, headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()
		return data
	except socket.error:
		return None
	except socket.timeout:
		return None

def get(address,uri):
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	try:
		conn = httplib.HTTPConnection(address,timeout=3)
		conn.request("GET", uri)
		response = conn.getresponse()
		data = response.read()
		conn.close()
		return data
	except socket.error:
		return None
	except socket.timeout:
		return None
		
