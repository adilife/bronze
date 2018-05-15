#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.
#取得CPU相关信息
#CPU time


import time
import cpu
import logdata
from common import DelLastChar

#保存cputimes
tuple_cpu_times=cpu.cpu_times()
writestr=str(time.strftime("%Y-%m-%d %X",time.localtime()))+", "+str(tuple_cpu_times)+"\n"
logdata.writelog("cputimes", writestr)

#保存 cpu percent
tcc=cpu.cpu_percent(True)
tcc.insert(0,cpu.cpu_percent())

cn=cpu.cpu_name()
cn.insert(0,"avage")

pre_writestr=""
for i in range(0,len(tcc)):
    pre_writestr=pre_writestr+cn[i]+"="+str(tcc[i])+", "

pre_writestr=DelLastChar(DelLastChar(pre_writestr))
writestr=str(time.strftime("%Y-%m-%d %X",time.localtime()))+", "+pre_writestr+"\n"
logdata.writelog("cpupercent", writestr)






