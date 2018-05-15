#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.
#取得CPU相关信息
#CPU time


import psutil
import time
import os

class cpu(object):
    #def __init__(self, *args, **kwargs):

    def cpu_times(percpu=False):
        return psutil.cpu_times(percpu)
        #scputimes(user=3317.13, nice=0.21, system=1353.57, idle=52900.49, iowait=1207.56, irq=0.0, softirq=37.21,\
        # steal=0.0, guest=0.0, guest_nice=0.0)

    def cpu_percent(percpu=False,interval=1):
        return psutil.cpu_percent(interval, percpu)


tuple_cpu_times=cpu.cpu_times()
name="cpuinfo_"+time.strftime('%Y%m%d',time.localtime(time.time()))



with open('log/'+name,'ta',encoding='utf-8',errors='ignore') as f:
    f.write("hel12lo\n")
    f.close()





