#!/usr/bin/python
import sys
import string

def from_ip(ip):
  segs=ip.split(".")
  result=0
  for part in segs:
    result+=str(bin(int(part))).count("1")
  return result	

def to_ip(mask):
  mask=int(mask)
  t="1"*mask
  t=t.ljust(32,"0")
  result=""
  for i in range(0,4):
    result+=str(string.atoi(t[i*8:(i+1)*8],2))+"."
  return  result[0:len(result)-1]	
