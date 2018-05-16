#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.

import psutil
import multiprocessing

class Cpu(object):
    def __init__(self):
        self.cpu_count=0
        self.cpu_name=[]
        self.__get()

    def __get(self):
        self.cpu_count=multiprocessing.cpu_count()
        for i in range(0,self.cpu_count):
            self.cpu_name.append("cpu"+str(i))
        return

class Cpu_percent(Cpu):
    def __init__(self):
        super().__init__()
        self.cpu_percent=[]

    def get(self, percpu=True, interval=1):
        self.cpu_percent=psutil.cpu_percent(interval, percpu)
        return self.cpu_percent

class Cpu_times(Cpu):
    def __init__(self):
        super().__init__()
        self.cpu_times=[]
        
    def get(self,percpu=False):
        #scputimes(user=3317.13, nice=0.21, system=1353.57, idle=52900.49, iowait=1207.56, irq=0.0, softirq=37.21,\
        # steal=0.0, guest=0.0, guest_nice=0.0)
        self.cpu_times=psutil.cpu_times(percpu)
        return self.cpu_times






