#!/bin/bash

a=`grep -Eo '^[^ ]+' it_app_vm.txt | sed -n '2p'`;
echo $a;

