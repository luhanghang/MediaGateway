import os
from httpClient import *

def to_bin(str, len):
	return bin(int(str)).lstrip('0b').zfill(len)

def backup1(filename):
	pass
	
def backup(filename):
	os.system('cp ' + filename + ' /tftpd')
	update_version()

def update_version():
	file=open('/tftpd/version')
	data=file.read()
	file.close()
	data=int(data)
	data+=1
	file=open('/tftpd/version','w')
	file.write(str(data))
	file.close()
