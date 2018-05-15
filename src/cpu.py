#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.


import multiprocessing
import psutil


def cpu_times(percpu=False):
    return psutil.cpu_times(percpu)
    #scputimes(user=3317.13, nice=0.21, system=1353.57, idle=52900.49, iowait=1207.56, irq=0.0, softirq=37.21,\
    # steal=0.0, guest=0.0, guest_nice=0.0)

def cpu_percent(percpu=False,interval=1):
    return psutil.cpu_percent(interval, percpu)
    
def cpu_name():
    #reture cpu name list
    _cpu_count=multiprocessing.cpu_count()
    _cpu_name=[]
    for i in range(0,_cpu_count):
        _cpu_name.append("cpu"+str(i))
    return _cpu_name



