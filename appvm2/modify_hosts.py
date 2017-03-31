#!/usr/bin/python
import subprocess
import sys
q=subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)
output,error=q.communicate()
#print output
a=open("/etc/hosts","a")
a.write("127.0.0.1 "+output+"\n")
a.close()

