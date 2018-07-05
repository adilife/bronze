#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.

'''



'''

import os,re
import psutil
from subprocess import Popen, PIPE


class Net_card(object):
    def __init__(self):
        self.nic_addr={}
        self.nic_stats={}
        self.nic_mac={}
        self.__nic_attr=[]
        self.nic_attr={}

        
        self.__get()
        return
    
    def __get(self):
        self.nic_addr=psutil.net_if_addrs()
        self.nic_stats=psutil.net_if_stats()
        self.__nic_attr=self.__get_nic_dev()
        self.nic_mac=self.__get_nic_mac()    

        for i in self.__nic_attr:
            for j in self.nic_mac.keys():
                if i[0] == self.nic_mac[j][0]:
                    self.nic_attr[j]=i




        return

    def __get_nic_dev(self):
        #use lspci -Dmm get pci info
        p=Popen('lspci -Dmm',shell=True,stdout=PIPE, stderr=PIPE).stdout.read().split(b"\n")
        nic_attr=[]
        for k,v in enumerate(p):
            a=v.decode("ascii")
            re_pci_addr=r'\d{4}:\d{2}:\d{2}.\d'
            re_pci_attr=r'(?<=").+?(?=")'
            re_pci_rev=r'-.+?(?=\s)'

            if a != "" :
                tmp_pci_addr=re.findall(re_pci_addr, a)
                tmp_pci_attr=re.findall(re_pci_attr,a)
                for k,v in enumerate(tmp_pci_attr):
                    if v==" " or v.strip()[0]=="-":
                        tmp_pci_attr.pop(k)
                tmp_pci_rev=re.findall(re_pci_rev,a)

                if tmp_pci_attr[0]=="Ethernet controller" :
                    nic_attr.append((tmp_pci_addr[0],tuple(tmp_pci_attr),tmp_pci_rev[0]))
        return nic_attr

    def __get_nic_mac(self):
        #use /sys/bus/pci/devices/0000:02:01.0/net/ens33/address to find nic name & mac addrsss
        nic_mac={}
        for v in self.__nic_attr:
            tmp_path_1="/sys/bus/pci/devices/%s/net/" % v[0]
            os.chdir(tmp_path_1)
            tmp_name=[x for x in os.listdir(".") if os.path.isdir(x)]
            tmp_path_2=os.path.join(tmp_path_1,tmp_name[0])
            file_path=os.path.join(tmp_path_2,"address")
            with open(file_path,'rt',encoding='utf-8',errors='ignore') as mf:
                tmp_mac=mf.read().strip("\n")
                mf.close()
            nic_mac[tmp_name[0]]=(v[0],tmp_mac)

        return nic_mac






a=Net_card()

for k,v in enumerate(a.__dict__.items()):
    print(k,v)
#print(a.nic_stats)
#print(psutil.net_connections())

#print(a.nic_name)





