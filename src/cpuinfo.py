#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.
#取得CPU相关信息
#CPU time


import time
import bronze_logdata
import bronze_cpu


#保存cputimes
cpu_times=bronze_cpu.Cpu_times()
pre_writestr=""
pre_writestr=str(cpu_times.get())
pre_writestr=pre_writestr[10:-1]
writestr=str(time.strftime("%Y-%m-%d %X",time.localtime()))+", "+pre_writestr+"\n"

logdata=bronze_logdata.Logdata()
logdata.set("cputimes",writestr)
logdata.writelog()

#保存 cpu percent
cpu_percent=bronze_cpu.Cpu_percent()
tcc=cpu_percent.get()
pc=0.0
for i,u in enumerate(tcc):
    pc+=int(u)
    ac=pc/cpu_percent.cpu_count
tcc.insert(0,ac)

cn=cpu_percent.cpu_name
cn.insert(0,"avage")

pre_writestr=""
for i,u in enumerate(tcc):
    pre_writestr=pre_writestr+cn[i]+"="+str(u)+", "
pre_writestr=pre_writestr[:-2]
writestr=str(time.strftime("%Y-%m-%d %X",time.localtime()))+", "+pre_writestr+"\n"

logdata=bronze_logdata.Logdata()
logdata.set("cpupercent",writestr)
logdata.writelog()





