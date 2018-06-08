#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.


import time
from bronze_lib.bronze_common import *

class Logdata(object):
    def __init__(self):
        self.content=""
        self.logtype=""
        self.__logtypelist=LOG_TYPE_LIST
        self.logfilepath=CONFIG_LOG_DIR+"log/"

    def set(self,logtype,content):
        if logtype in self.__logtypelist:
            self.logtype=logtype
            if isinstance(content, str):
                self.content=content
        return

    def writelog(self,method="logfile"):
        if method=="logfile":
            self.__writelog_file()
        return

    def __writelog_file(self):
        if self.logtype == "cpuinfo":
            #文件名按找日期生成，作为本地缓冲存储
            logname=self.logfilepath+self.logtype+"_"+time.strftime('%Y%m%d',time.localtime(time.time()))
            with open(logname,'ta',encoding='utf-8',errors='ignore') as myfile:
                myfile.write(self.content)
                myfile.close()
        elif self.logtype in ["osinfo","meminfo"]:
            #只生成1个文件
            logname=self.logfilepath+self.logtype
            with open(logname,'tw',encoding='utf-8',errors='ignore') as myfile:
                myfile.write(self.content)
                myfile.close()
        return


