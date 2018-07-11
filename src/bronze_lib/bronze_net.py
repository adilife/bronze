#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import sleep

#This file is a part of project Bronze.

'''
class Net_card()  ： 定义Net_card类
        nic_addr    :   IP地址
        nic_stats   ：  接口状态
        nic_mac     ：  MAC地址及PCI地址
        nic_attr    ：  网卡属性及接口名
        utilization(interval=5,period=2): 返回平均值 {网卡名：（接收速率，发送速率）}
'''

import os,re
import psutil
import time
from subprocess import Popen, PIPE


class Net_card(object):
    def __init__(self):
        self.nic_addr={}
        self.nic_stats={}
        self.nic_mac={}
        self.nic_attr={}
        
        self.__get()
        return
    
    def __get(self):
        self.nic_addr=psutil.net_if_addrs()
        self.nic_stats=psutil.net_if_stats()
        self.nic_attr=self.__get_nic_dev()
        self.nic_mac=self.__get_nic_mac()    

        for i in self.nic_attr.keys():
            for j in self.nic_mac.keys():
                if i == self.nic_mac[j][0]:
                    self.nic_attr[i].insert(0,j)

        return

    def __get_nic_dev(self):
        #use lspci -Dmm get pci info
        p=Popen('lspci -Dmm',shell=True,stdout=PIPE, stderr=PIPE).stdout.read().split(b"\n")
        nic_attr={}
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
                    #nic_attr.append([tmp_pci_addr[0],tmp_pci_attr,tmp_pci_rev[0]])
                    nic_attr[tmp_pci_addr[0]]=[tmp_pci_attr,tmp_pci_rev[0]]
        return nic_attr

    def __get_nic_mac(self):
        #use /sys/bus/pci/devices/0000:02:01.0/net/ens33/address to find nic name & mac addrsss
        nic_mac={}
        for v in self.nic_attr.keys():
            tmp_path_1="/sys/bus/pci/devices/%s/net/" % v
            os.chdir(tmp_path_1)
            tmp_name=[x for x in os.listdir(".") if os.path.isdir(x)]
            tmp_path_2=os.path.join(tmp_path_1,tmp_name[0])
            file_path=os.path.join(tmp_path_2,"address")
            with open(file_path,'rt',encoding='utf-8',errors='ignore') as mf:
                tmp_mac=mf.read().strip("\n")
                mf.close()
            nic_mac[tmp_name[0]]=(v,tmp_mac)

        return nic_mac

    def utilization(self,interval=5,period=2):
        #周期抓取信息
        trdata=[]
        i=0
        #print("NIC{:5s} : {:5s} re/bytes {:10s} tr/bytes".format("","",""))
        while i < interval:
            i = i+1
            tmp_trdata=self.__get_net_tr()
            trdata.append(tmp_trdata)
            #for k,v in enumerate(tmp_trdata.items()):
                #print("{:8s} :     {:20s} {}".format(v[0],v[1][0],v[1][1]))
            if i < interval:
                sleep(period)
        #处理抓取的信息，分解出接收/发送/时间戳，用于后续处理
        util={}
        recive={}
        tran={}
        ptime={}
        for k,v in enumerate(trdata[0].keys()):
            recive[v]=int(trdata[interval-1][v][0])-int(trdata[0][v][0])
            tran[v]=int(trdata[interval-1][v][1])-int(trdata[0][v][1])
            ptime[v]=trdata[interval-1][v][2]-trdata[0][v][2]
            if ptime[v] == 0:
                #避免时间周期为 0
                print("Time is zero.")
                exit()
        #计算时间周期内B/s的值
        for k,v in  enumerate(recive.keys()):
            util_re=recive[v]/ptime[v]
            util_tr=tran[v]/ptime[v]
            util[v]=(util_re,util_tr)
        #返回平均值 {网卡名：（接收速率，发送速率）}
        return util

    def __get_net_tr(self):
        trdata={}
        with open('/proc/net/dev','tr',encoding='utf-8',errors='ignore') as myfile:
            for line in myfile.readlines():
                dl=line.strip().split(":")
                if dl[0].strip() in self.nic_mac.keys():
                    dd=dl[1].split()
                    trdata[dl[0]]=(dd[0],dd[8],int(time.time()))
            myfile.close()
        return trdata





