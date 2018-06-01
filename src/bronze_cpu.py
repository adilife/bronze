#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.

import psutil
import multiprocessing
import platform

class Cpu(object):
    def __init__(self):
        self.cpu_count=0
        self.cpu_name=[]
        self.cpu_model=[]
        self.cpu_freq=[]
        
        self.__get()

    def __get(self):
        self.__get_cpu_base_info()
        return
    
    def __get_cpu_name(self):
        if self.cpu_count == 0:
            self.cpu_count=multiprocessing.cpu_count()
        for i in range(0,self.cpu_count):
            self.cpu_name.append("cpu"+str(i))
        return

    def __get_cpu_base_info(self):
        self.__get_cpu_name()
        
        __sysstr = platform.system()
        if __sysstr == "Linux":
            self.__get_linux_cpu_base_info()

        return

    def __get_linux_cpu_base_info(self):
        #打开实际的 \proc\cpuinfo 文件需要用root用户运行
        with open(r'/proc/cpuinfo','tr',errors='ignore') as cf:
            for line in cf:
                if line.startswith('cpu MHz'):
                    self.cpu_freq.append(float(line.split(':')[1].strip()))
                if line.startswith('model name'):
                    self.cpu_model.append(line.split(':')[1].strip())
            cf.close()
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




