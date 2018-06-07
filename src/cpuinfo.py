#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.
#取得CPU相关信息
#CPU time


import time
import sys, getopt

#import bronze mod
import bronze_logdata
import bronze_cpu
from bronze_common import *


#处理命令行参数 -h/--help 打印帮助信息，无参数/-w/--write 保存LOG文件，-s/--show 只显示信息，不保存, -l/-logfile = 指定日志存储位置
def main(argv):
    log_file = ''
    show_argv = ''
        
    try:
        opts, args = getopt.getopt(argv,"hws:l:",["help","write","show=","logfile="])
    except getopt.GetoptError:
        print("wrong args!")
        __usage()
        exit()

    #命令行无参数处理
    if opts==[] :
        print("no args,default write logs")
        __write_log()
        
    #命令行参数处理
    else:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                __usage()
                exit()
            elif opt in ("-w", "--write"):
                print("write argv")
                __write_log()
            elif opt in ("-s", "--show"):
                show_argv = arg
                __show_info(show_argv)
                exit()
            elif opt in ("-l", "--logfile"):
                log_file = arg
                print("logfile")

def __write_log():
    #保存cputimes
    cpu_times=bronze_cpu.Cpu_times()
    pre_writestr=""
    pre_writestr=str(cpu_times.get())
    pre_writestr=pre_writestr[10:-1]
    cputimes_writestr=str(time.strftime("%Y-%m-%d %X",time.localtime()))+"# cputimes# "+pre_writestr+"\n"

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
    cpupercent_writestr=str(time.strftime("%Y-%m-%d %X",time.localtime()))+"# cpupercent# "+pre_writestr+"\n"

    writestr=cputimes_writestr+cpupercent_writestr 
    logdata=bronze_logdata.Logdata()
    logdata.set("cpuinfo",writestr)
    logdata.writelog()

def __usage():
    usage_content=\
'''
usage cpuinfo.py [-hswl | --help --write --show <[cpu_times|times]|[cpu_percent|percent]> --logfile path_name]

-h/--help 打印帮助信息
无参数/-w/--write 保存LOG文件
-s/--show 只显示信息，不保存
    cpu_times | times 显示cpu times信息
    cpu_percent | percent 显示 cpu percent信息
-l/-logfile = 指定日志存储位置, 未完成
'''
    print(usage_content)

def __show_info(st):
    #show cpu_times
    if st=="cpu_times" or st == "times" :
        cpu_times=bronze_cpu.Cpu_times()
        pre_writestr=""
        pre_writestr=str(cpu_times.get())
        pre_writestr=pre_writestr[10:-1]
        writestr=str(time.strftime("%Y-%m-%d %X",time.localtime()))+"# "+pre_writestr+"\n"
        print(writestr)
    elif st=="cpu_percent" or st == "percent":
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
        writestr=str(time.strftime("%Y-%m-%d %X",time.localtime()))+"# "+pre_writestr+"\n"
        print(writestr)
    else :
        print("wrong args!")
        __usage()


if __name__ == "__main__" :
    check_platform(PLATFORM) #监测运行平台是否符合要求
    main(sys.argv[1:])



