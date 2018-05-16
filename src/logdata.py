#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.

import psutil
import time


def logtypelist():
    _logtypelist=["cputimes","cpupercent","meminfo"]
    return _logtypelist

def writelog(logtype,writestr):
    if isinstance(logtype,str):
        if logtype in logtypelist():
            logname='log/'+logtype+"_"+time.strftime('%Y%m%d',time.localtime(time.time()))
        return
        
    if isinstance(writestr,str):
        #'log/' 输出文件保存路径
        #文件名按找日期生成，作为本地缓冲存储
        with open(logname,'ta',encoding='utf-8',errors='ignore') as myfile:
            myfile.write(writestr)
            myfile.close()
        return

