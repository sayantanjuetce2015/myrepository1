#!/usr/bin/python
import json
import sys
import subprocess
import logging
import time


# Update access details for ECM
vz_update_user="vzdevops"
vz_update_passwd="vzdevops.123"
vz_update_ecmip="10.111.148.125"


#Syntax for creating VDC
total=len(sys.argv)
cmdargs=str(sys.argv)
if (total<3):
   print "syntax:delete_VM.py <tenant_name> <vdc_name>"
   exit()
tenant_name=sys.argv[1]
vdc_name=sys.argv[2]

#GEt vdc_id
command_string = "curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantID:"+tenant_name+"\"  -H \"Content-type: application/json\" -X GET http://"+vz_update_ecmip+":8080/ecm_service/vdcs"
#print command_string
p = subprocess.Popen(command_string, stdout=subprocess.PIPE, shell=True)
(output,err)=p.communicate()
#print output
data=json.loads(output)
vdc_data=data["data"]["vdcs"]
i=0
try:
   while(vdc_data[i]):
      if(vdc_data[i]["name"]==vdc_name):
         vdc_id=vdc_data[i]["id"]
         print "VDC ID : ",vdc_id
         break
      i=i+1
except IndexError:
   print "VDC not found "
   exit(0)


#GEt vm details
command_string = "curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantID:"+tenant_name+"\"  -H \"Content-type: application/json\" -X GET http://"+vz_update_ecmip+":8080/ecm_service/vdcs/"+vdc_id
#print command_string
p = subprocess.Popen(command_string, stdout=subprocess.PIPE, shell=True)
(output,err)=p.communicate()
#print output
data=json.loads(output)
try:
   vms_data=data["data"]["vdc"]["vms"]
except KeyError:
   print "No VMs in the VDC"
   exit(0)
j=0
vm_id_list=[]
vm_name_list=[]      
try:
   while(vms_data[j]):
      vm_id=vms_data[j]["id"]
      vm_id_list.append(vm_id)
      vm_name=vms_data[j]["name"]
      vm_name_list.append(vm_name)
      j=j+1
except IndexError:
   print "Extraction of VM details complete..."
   vm_id_list_len=len(vm_id_list)
   #print vm_id_list_len


#Delete VM's
for i in range(0,vm_id_list_len):
   print "Deleting VM with id:",vm_id_list[i]
   posturl="http://"+vz_update_ecmip+":8080/ecm_service/vms/"+vm_id_list[i]
   #print posturl
   command_string = "curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantID:"+tenant_name+"\" -H \"Content-type: application/json\" -X DELETE "+posturl
   #print command_string
   p=subprocess.Popen(command_string, stdout=subprocess.PIPE, shell=True)
   (output,err)=p.communicate()
   #print output
   data=json.loads(output)
   order_id=data["data"]["order"]["id"]
   print "Order id : ",order_id
   command_string="curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantId:"+tenant_name+"\" -H \"Content-type: application/json\" -X GET http://"+vz_update_ecmip+":8080/ecm_service/orders/"+order_id
   #print command_string
   p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
   output,err=p.communicate()
   #print output
   data=json.loads(output)
   order_req_status=data["data"]["order"]["orderReqStatus"]
   #print "Present Order Request Status : ",order_req_status
   while(order_req_status!="COM"):
      print "==============================================================================================================\n"
      print "Present Status of VM deletion Order: \n"
      print order_req_status
      print "==============================================================================================================\n"
      if(order_req_status=="ERR"):
         print "==============================================================================================================\n"
         print "Error occured during deletion of VM: \n",vm_name_list[i]
         print "==============================================================================================================\n"
         #exit(0)
      time.sleep(5)
      p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
      output,err=p.communicate()
      #print output
      data=json.loads(output)
      order_req_status=data["data"]["order"]["orderReqStatus"]
      #print "Present Order Request Status : ",order_req_status
   print "==============================================================================================================\n"
   print "Present Status of VM deletion Order: \n"
   print order_req_status
   print "==============================================================================================================\n"
   print "VM deletion success for ",vm_name_list[i]
            
   


