#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.



#定义配置项
CONFIG_LOG_DIR="./"
LOG_TYPE_LIST=["cputimes","cpupercent","meminfo"]
PLATFORM="Linux"  #当前操作系统平台

#定义监测操作系统版本方法
def check_platform(pf):
    import platform
    if platform.system() != pf :
        print("This version only support %s." % pf)
        exit()





