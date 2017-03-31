#!/usr/bin/python
import json
import subprocess
import sys
import logging

#user details
username="GEAdmin"
password="GEAdmin123"
ecmip="10.118.47.149"

#syntax for checking all the VMs
total=len(sys.argv)
cmdargs=str(sys.argv)
if(total<4):
   print "syntax:Get_IP_of_VM.py <tenantname> <VM_name> <VM_type>"
   exit(0)

#Tenantname and status from input parameters
tenantname=sys.argv[1]
vm_name=sys.argv[2]
vm_type=sys.argv[3]

#Get vm_id using vm_name
command_string="curl -u "+username+":"+password+" -H \"TenantId:"+tenantname+"\" -H \"Content-type: application/json\" -X GET http://"+ecmip+":8080/ecm_service/vms/"
#print command_string
print "**************************************************************"
print "GET From REST URI: /vms To Get List Of VM Present In The ECM"
print "**************************************************************"
p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
output,err=p.communicate()
#print output
data=json.loads(output)
#print data
vm_data=data["data"]["vms"]
i=0
try:
   while(vm_data[i]):
      if(vm_data[i]["name"]==vm_name):
         vm_id=vm_data[i]["id"]
         break
      i=i+1
except IndexError:
   print "VM not found"
   exit(0)

#get vmvnics_id using vm_id
command_string="curl -u "+username+":"+password+" -H \"TenantId:"+tenantname+"\" -H \"Content-type: application/json\" -X GET http://"+ecmip+":8080/ecm_service/vms/"+vm_id
#print command_string
print "**************************************************************"
print "GET From REST URI: /vms/<vm_id> To Get Details Of VM : ",vm_name
print "**************************************************************"
p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
output,err=p.communicate()
#print output
data=json.loads(output)
#print data
vmvnics_id=data["data"]["vm"]["vmVnics"][0]["id"]
#print vmvnics_id


#Get IP address using vmvnics_id
command_string="curl -u "+username+":"+password+" -H \"TenantId:"+tenantname+"\" -H \"Content-type: application/json\" -X GET http://"+ecmip+":8080/ecm_service/vmvnics/"+vmvnics_id
#print command_string
print "**************************************************************"
print "GET From REST URI: /vmvnics/<vmvnics_id> To Get Details of vmvnics : ",vmvnics_id
print "**************************************************************"
p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
output,err=p.communicate()
#print output
data=json.loads(output)
#print data
vm_ip=data["data"]["vmVnic"]["internalIpAddress"][0]
#print vm_ip
vm_data=open("/home/ubuntu/ge_poc_it_app/"+str(vm_type)+".txt","w")
server_name="["+vm_type+"]\n"
ip_user_passwd=vm_ip+" ansible_ssh_user=cloud ansible_ssh_pass=ericsson\n"
vm_data.write(server_name)
vm_data.write(ip_user_passwd)
vm_data.close()




