import httpClient

def read_conf():
	file = open('/etc/record_server')
	data = file.read()
	file.close()
	return data.strip()
	
def test_connection():
	url = read_conf()
	data = httpClient.get(url,'/test_connection.html')
	if data == 'JxRecord':
		return url
	return 0
