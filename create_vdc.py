#!/usr/bin/python
import json
import subprocess
import sys
import logging
import time


#user details
vz_update_user="vzdevops"
vz_update_passwd="vzdevops.123"
vz_update_ecmip="10.111.148.125"


#Syntax for creating VDC
total=len(sys.argv)
cmdargs=str(sys.argv)
if(total<6):
   print "syntax:create_vdc.py <tenantname> <vim_zone> <vdc_name> <quantity_value> <flavor_value>"
   exit(0)


#Tenantname vim_zone vdc_name quantity_value and flavor_value from input parameters
tenantname=sys.argv[1]
vim_zone=sys.argv[2]
vdc_name=sys.argv[3]
quantity_value=sys.argv[4]
flavor_value=sys.argv[5]


#Create VDC and get order_id
posturl="http://"+vz_update_ecmip+":8080/ecm_service/vdcs"
#print posturl
command_string="curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantId:"+tenantname+"\" -H \"Content-type: application/json\" -X POST "+posturl+" -d '{\"tenantName\":\""+tenantname+"\",\"customOrderParams\":[{\"tag\":\"quantity\",\"value\":\""+quantity_value+"\"},{\"tag\":\"flavor\",\"value\":\""+flavor_value+"\"}],\"vdc\":{\"name\":\""+vdc_name+"\",\"vimZoneName\":\""+vim_zone+"\"}}'"
#print command_string
p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
output,err=p.communicate()
#print output
data=json.loads(output)
order_id=data["data"]["order"]["id"]
print "VDC Create Order ID:",order_id


#Check Order Status and get vdc_id by querying orders with order_id 
command_string="curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantId:"+tenantname+"\" -H \"Content-type: application/json\" -X GET http://"+vz_update_ecmip+":8080/ecm_service/orders/"+order_id
#print command_string
p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)        
output,err=p.communicate()
#print output
data=json.loads(output)
order_req_status=data["data"]["order"]["orderReqStatus"]
#print "Present Order Request Status : ",order_req_status
while(order_req_status!="COM"):
   print "==============================================================================================================\n"
   print "Present Status of VDC creation Order: \n"
   print order_req_status
   print "==============================================================================================================\n"
   if(order_req_status=="ERR"):
       print "==============================================================================================================\n"
       print "Error occured during creation of VDC: \n"
       print "==============================================================================================================\n"
       exit(0)

   time.sleep(5)
   p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
   output,err=p.communicate()
   #print output
   data=json.loads(output)
   order_req_status=data["data"]["order"]["orderReqStatus"]
   #print "Present Order Request Status : ",order_req_status
print "==============================================================================================================\n"
print "Present Status of VDC creation Order: \n"
print order_req_status
print "==============================================================================================================\n"
vdc_id=data["data"]["order"]["orderItems"][0]["createVdc"]["id"]
print "VDC ID : ",vdc_id


#Check VDC status
command_string="curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantId:"+tenantname+"\" -H \"Content-type: application/json\" -X GET http://"+vz_update_ecmip+":8080/ecm_service/vdcs/"+vdc_id
#print command_string
p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
output,err=p.communicate()
#print output
data=json.loads(output)
vdc_status=data["data"]["vdc"]["provisioningStatus"]
print "==============================================================================================================\n"
print "Present Status of VDC : \n"
print vdc_status
print "==============================================================================================================\n"
while(vdc_status!="ACTIVE"):
   time.sleep(180)
   p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
   output,err=p.communicate()
   #print output
   data=json.loads(output)
   vdc_status=data["data"]["vdc"]["provisioningStatus"]
   print "==============================================================================================================\n"
   print "Present Status of VDC : \n"
   print vdc_status
   print "==============================================================================================================\n"




