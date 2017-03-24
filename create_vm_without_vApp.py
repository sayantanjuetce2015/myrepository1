#!/usr/bin/python
import json
import subprocess
import sys
import logging

#user details
vz_update_user="vzdevops"
vz_update_passwd="vzdevops.123"
vz_update_ecmip="10.111.148.125"

### TO update later
vnicsname="eth0"
vnname="test_vn"

#syntax for creating vm
total=len(sys.argv)
cmdargs=str(sys.argv)
#if(total<7):
   #print "syntax:create_vm.py <tenantname> <vdc-name> <image_name> <vm_name> <vmhd_name> <vapp_name>"
   #exit(0)
if(total<6):
   print "To create a standalone VM : "
   print "syntax:create_vm.py <tenantname> <vdc-name> <image_name> <vm_name> <vmhd_name>"
   print "To create VM associated with a VAPP : "
   print "syntax:create_vm.py <tenantname> <vdc-name> <image_name> <vm_name> <vmhd_name> <vapp_name>"
   exit(0)
#Tenantname,vdcname,imagename,vmname,vmhdname,vappname from input parameters
tenantname=sys.argv[1]
vdcname=sys.argv[2]
imagename=sys.argv[3]
vmname=sys.argv[4]
vmhdname=sys.argv[5]
if(total==6):
   print "You are creating a VM which will not be associated with any VAPP"
if(total==7):
   vappname=sys.argv[6]

#get VN id from VN name
command_string = "curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantID:"+tenantname+"\"  -H \"Content-type: application/json\" -X GET http://"+vz_update_ecmip+":8080/ecm_service/vns"
#print command_string
p = subprocess.Popen(command_string, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
#print output
data=json.loads(output)
vndata=data["data"]["vns"]
i=0
try:
   while(vndata[i]):
      #print pkgdata[i]["name"]
      if(vndata[i]["name"] == vnname):
         vnid=vndata[i]["id"]
         print "VNid:",vnid
         break
      i=i+1
except IndexError:
   print "VN not found"
   exit(0)


#get VDC id
command_string="curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantId:"+tenantname+"\" -H \"Content-type: application/json\" -X GET http://"+vz_update_ecmip+":8080/ecm_service/vdcs"
#print command_string
p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
(output,err)=p.communicate()
#print output
data=json.loads(output)
vdcdata=data["data"]["vdcs"]
i=0
try:
   while(vdcdata[i]):
      if(vdcdata[i]["name"]==vdcname):
         vdc_id=vdcdata[i]["id"]
         print "VDC_id : ",vdc_id
         break
      i=i+1

except IndexError:
   print "VDC not found"
   exit(0)

#get Vapp id
if(total==7):
   command_string="curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantId:"+tenantname+"\" -H \"Content-type: application/json\" -X GET http://"+vz_update_ecmip+":8080/ecm_service/vapps"
   #print command_string
   p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)        
   output,err=p.communicate()
   #print output
   data=json.loads(output)
   vappdata=data["data"]["vapps"]
   j=0
   try:
      while(vappdata[j]):
         if(vappdata[j]["name"]==vappname):
            vapp_id=vappdata[j]["id"]
            print "VAPP_id : ",vapp_id
            break
         j=j+1
   except IndexError:
      print "VAPP not found"
      exit(0)


#create vm which will be associated with VAPP
if(total==7):
   posturl="http://"+vz_update_ecmip+":8080/ecm_service/vms"
   json_to_create_vm="{\"tenantName\":\""+tenantname+"\",\"vm\":{\"name\":\""+vmname+"\",\"bootSource\":{\"imageName\":\""+imagename+"\"},\"vmhdName\":\""+vmhdname+"\",\"vdc\":{\"id\":\""+vdc_id+"\"},\"vapp\":{\"id\":\""+vapp_id+"\"},\"vmVnics\":[{\"name\":\""+vnicsname+"\",\"vn\":{\"id\":\""+vnid+"\"}}]}}"
   command_string="curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantId:"+tenantname+"\" -H \"Content-type: application/json\" -X POST "+posturl+" -d '"+json_to_create_vm+"'"
   print command_string
   p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
   output,err=p.communicate()
   print output
   data=json.loads(output)
   order_id=data["data"]["order"]["id"]
   print "VM Create Order ID:",order_id


#Get Order status
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
      print "Present Status of VM creation Order: \n"
      print order_req_status
      print "==============================================================================================================\n"
      if(order_req_status=="ERR"):
          print "==============================================================================================================\n"
          print "Error occured during creation of VM: \n"
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
   print "Present Status of VM creation Order: \n"
   print order_req_status
   print "==============================================================================================================\n"

#Create a standalone VM
if(total==6):
   posturl="http://"+vz_update_ecmip+":8080/ecm_service/vms"
   json_to_create_vm="{\"tenantName\":\""+tenantname+"\",\"vm\":{\"name\":\""+vmname+"\",\"bootSource\":{\"imageName\":\""+imagename+"\"},\"vmhdName\":\""+vmhdname+"\",\"vdc\":{\"id\":\""+vdc_id+"\"},\"vmVnics\":[{\"name\":\""+vnicsname+"\",\"vn\":{\"id\":\""+vnid+"\"}}]}}"
   command_string="curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantId:"+tenantname+"\" -H \"Content-type: application/json\" -X POST "+posturl+" -d '"+json_to_create_vm+"'"
   print command_string
   p=subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
   output,err=p.communicate()
   print output
   data=json.loads(output)
   order_id=data["data"]["order"]["id"]
   print "VM Create Order ID:",order_id

#Get Order status
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
      print "Present Status of VM creation Order: \n"
      print order_req_status
      print "==============================================================================================================\n"
      if(order_req_status=="ERR"):
          print "==============================================================================================================\n"
          print "Error occured during creation of VM: \n"
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
   print "Present Status of VM creation Order: \n"
   print order_req_status
   print "==============================================================================================================\n"
