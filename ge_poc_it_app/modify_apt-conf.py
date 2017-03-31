#!/usr/bin/python
import subprocess
import sys
proxy_ip="10.118.0.48"
proxy_port="3128"
a=open("/etc/apt/apt.conf","a")
proxy_http="Acquire::http::proxy \"http://"+proxy_ip+":"+proxy_port+"/\";"
proxy_https="Acquire::https::proxy \"https://"+proxy_ip+":"+proxy_port+"/\";"
#print b
a.write(proxy_http+"\n")
a.write(proxy_https+"\n")
a.close()

