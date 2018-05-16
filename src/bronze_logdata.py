#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.


import time

class Logdata(object):
    def __init__(self):
        self.content=""
        self.logtype=""
        self.__logtypelist=["cputimes","cpupercent","meminfo"]
        self.logfilepath="log/"

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
        #文件名按找日期生成，作为本地缓冲存储
        logname=self.logfilepath+self.logtype+"_"+time.strftime('%Y%m%d',time.localtime(time.time()))
        with open(logname,'ta',encoding='utf-8',errors='ignore') as myfile:
            myfile.write(self.content)
            myfile.close()
        return

