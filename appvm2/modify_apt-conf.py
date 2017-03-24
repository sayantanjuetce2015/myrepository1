#!/usr/bin/python
import subprocess
import sys
proxy_ip="10.7.0.140"
proxy_port="8081"
a=open("/etc/apt/apt.conf","a")
proxy="Acquire::http::proxy \"http://"+proxy_ip+":"+proxy_port+"/\";"
#print b
a.write(proxy+"\n")
a.close()

