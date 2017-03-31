#!/usr/bin/python
import time
import json
import re
import sys
import subprocess
import time
import logging
import datetime
import os

### update following details before running this script
vz_update_user="GEAdmin"
vz_update_passwd="GEAdmin123"
vz_update_ecmip="10.118.47.149"
#vz_update_jenkins_testJob_build_url="10.111.148.164:8080/job/TestOVFonECM/build"
vz_update_jenkins_testJob_build_url="vzdevops:vzdevops.123@10.111.148.164:8080/job/TestOVFonECM/build"
vz_update_jenkins_user="vzdevops"
vz_update_jenkins_passwd="vzdevops.123"

total = len(sys.argv)
cmdargs=str(sys.argv)
#print cmdargs

if (total<4):
   print "syntax: deploy_ovfpkg.py <tenant> <PackageName> <Vdc-name>"
   exit()

tenantname = sys.argv[1]
pkgname = sys.argv[2]
vdcname = sys.argv[3]

#Get the VDC id from the VDC name
command_string = "curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantID:"+tenantname+"\"  -H \"Content-type: application/json\" -X GET http://"+vz_update_ecmip+":8080/ecm_service/vdcs"
#print command_string
print "**************************************************************"
print "GET From REST URI: /vdcs To Get List Of VDC Present In The ECM"
print "**************************************************************"
p = subprocess.Popen(command_string, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
#print output
data=json.loads(output)
vdcdata=data["data"]["vdcs"]
i=0
try:
   while(vdcdata[i]):
      #print pkgdata[i]["name"]
      if(vdcdata[i]["name"] == vdcname):
         vdcid=vdcdata[i]["id"]
      i=i+1
except IndexError:
   print "Looping Success"

#print tenantname

#create the subscription for the ECM notification
#if pkgname=='EVR02':
#   posturl="http://"+vz_update_ecmip+":8080/ecm_service/subscriptions"
#   command_string = "curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantID:"+tenantname+"\" -H \"Content-type: application/json\" -X POST "+posturl+" -d '{\"tenantName\":\""+tenantname+"\",\"eventType\":\"OrderComplete\",\"destType\":\"HTTP\",\"destAlias\":\"Jenkins\",\"params\":[{\"tag\":\"destinationAddress\",\"value\":\""+vz_update_jenkins_testJob_build_url+"\"},{\"tag\":\"destinationCredential\",\"value\":\""+vz_update_jenkins_user+"\"},{\"tag\":\"destinationPasswd\",\"value\":\""+vz_update_jenkins_passwd+"\"}]}'"
   #command_string = "curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantID:"+tenantname+"\" -H \"Content-type: application/json\" -X POST "+posturl+" -d '{\"tenantName\":\""+tenantname+"\",\"eventType\":\"OrderComplete\",\"destType\":\"HTTP\",\"destAlias\":\"Jenkins\",\"params\":[{\"tag\":\"destinationAddress\",\"value\":\""+vz_update_jenkins_testJob_build_url+"\"}]}'"
#   print command_string
#   p = subprocess.Popen(command_string, stdout=subprocess.PIPE, shell=True)
#   (output, err) = p.communicate()
#   print output


#Get OVF package details
command_string = "curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantID:"+tenantname+"\"  -H \"Content-type: application/json\" -X GET http://"+vz_update_ecmip+":8080/ecm_service/ovfpackages"
#print command_string
print "**************************************************************"
print "GET From REST URI: /ovfpackages To Get List Of Packages Present In ECM"
print "**************************************************************"
p = subprocess.Popen(command_string, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
#print output
data=json.loads(output)
pkgdata=data["data"]["ovfPackages"]
i=0
try:
   while(pkgdata[i]):
      #print pkgdata[i]["name"]
      if(pkgdata[i]["name"] == pkgname):
         pkgid=pkgdata[i]["id"]
         #print pkgid
         #Deploy the package
         posturl="http://"+vz_update_ecmip+":8080/ecm_service/ovfpackages/"+pkgid+"/deploy"
         #print posturl
         command_string = "curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantID:"+tenantname+"\" -H \"Content-type: application/json\" -X POST "+posturl+" -d '{\"tenantName\":\""+tenantname+"\",\"vdc\":{\"id\":\""+vdcid+"\"}}'"
         #print command_string
         print "**************************************************************"
         print "POST to REST URI: ovfpackages/<pkgid>/deploy To Deploy OVF File On ECM"
         print "**************************************************************"
         p = subprocess.Popen(command_string, stdout=subprocess.PIPE, shell=True)
         (output, err) = p.communicate()
         print output
         data=json.loads(output)
         order_id= data["data"]["order"]["id"]
      i=i+1
except IndexError:
   print "Looping Success"


#Get Order status
   command_string="curl -u "+vz_update_user+":"+vz_update_passwd+" -H \"TenantId:"+tenantname+"\" -H \"Content-type: application/json\" -X GET http://"+vz_update_ecmip+":8080/ecm_service/orders/"+order_id
   #print command_string
   print "**************************************************************"
   print "GET From REST URI: /orders/<order_id> To Get Status Of The Order"
   print "**************************************************************"
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
      print "**************************************************************"
      print "GET From REST URI: /orders/<order_id> to Get Status Of The Order"
      print "**************************************************************"
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
