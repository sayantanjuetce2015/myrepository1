#!/usr/bin/python
import json
import sys
import subprocess
import time
import logging


#Update access details for ECM
vz_update_user="vzdevops"
vz_update_passwd="vzdevops.123"
vz_update_ecmip="10.111.148.125"


#Syntax for deleting VDC
total=len(sys.argv)
cmdargs=str(sys.argv)
if (total<5):
   print "syntax: delete_vdc.py <tenant_name> <vdc_name> <quantity_value> <flavor_value>"
   exit(0)
tenant_name = sys.argv[1]
vdc_name = sys.argv[2]
quantity_value=sys.argv[3]
flavor_value=sys.argv[4]

#Get vdc_id
command_string = "curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantID:"+tenant_name+"\"  -H \"Content-type: application/json\" -X GET http://"+vz_update_ecmip+":8080/ecm_service/vdcs"
#print command_string
p=subprocess.Popen(command_string, stdout=subprocess.PIPE, shell=True)
(output,err)=p.communicate()
#print output
data=json.loads(output)
vdc_data=data["data"]["vdcs"]
i=0
try:
   while(vdc_data[i]):
      if(vdc_data[i]["name"]==vdc_name):
         vdc_id=vdc_data[i]["id"]
         #print vdc_name
         print "VDC ID : ",vdc_id
         break
      i=i+1
except IndexError:
   print "VDC not found"
   exit(0)


#Modify VDC CustomOrderParams
posturl="http://localhost:8090/cwf/api/jenkins-jenkinsInterface/scaleOut/"+vdc_id
#print posturl
command_string="curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantId:"+tenantname+"\" -H \"Content-type: application/json\" -X POST "+posturl+" -d '{\"quantity\":\""+quantity_value+"\",\"flavor\":\""+flavor_value+"\"}'"
#print command_string
p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
output,err=p.communicate()
#print output
data=json.loads(output)
status=data["Status"]
print "Status : ",status


#Get EOC status
command_string = "curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantID:"+tenant_name+"\"  -H \"Content-type: application/json\" -X GET http://localhost:8090/cwf/api/jenkins-jenkinsInterface/vdcs/"+vdc_id
#print command_string
p=subprocess.Popen(command_string, stdout=subprocess.PIPE, shell=True)
(output,err)=p.communicate()
#print output
data=json.loads(output)
state=data["state"]
print "State : ",state

while(state!="DEPLOYED"):
   print "==============================================================================================================\n"
   print "Present State : \n"
   print state
   print "==============================================================================================================\n"
   if(state=="ERROR"):
       print "==============================================================================================================\n"
       print "Error occured during modification of VDC: \n"
       print "==============================================================================================================\n"
       exit(0)

   time.sleep(5)
   p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
   output,err=p.communicate()
   #print output
   data=json.loads(output)
   state=data["state"]
   #print "Present Order Request Status : ",order_req_status
print "==============================================================================================================\n"
print "Present State : \n"
print state
print "==============================================================================================================\n"


