#!/usr/bin/python
import subprocess
import sys

#Syntax for creating VDC
total=len(sys.argv)
cmdargs=str(sys.argv)
if(total<2):
   print "syntax:ITAPP_test.py <APP_VM_IP>"
   exit(0)


appvmip=sys.argv[1]


command_string="sudo curl http://"+appvmip+":8080/"
print command_string
q=subprocess.Popen("export no_proxy="+appvmip, shell=True, stdout=subprocess.PIPE)
out,err=q.communicate()
#print out
p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)        
output,err=p.communicate()
#print output
if 'Todolist MVC is a web-based task manager' in output:
   print "Test Success: web page found!!"
else:
   print "Test Failed !!"
