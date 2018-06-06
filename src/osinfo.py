#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.

import time
import sys, getopt

#import bronze mod
import bronze_logdata
import bronze_os
from bronze_common import *
from asyncore import write

#处理命令行参数 -h/--help 打印帮助信息，-w/--write 保存LOG文件，-s/--show 只显示信息，不保存, -l/-logfile = 指定日志存储位置
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
        print("no args!")
        __usage()
        exit()
    
    else:
        #命令行参数处理
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

    return

def __write_log():

    #保存osinfo
    oi=bronze_os.OSinfo()
    osinfo_pre_writestr="OS_SYSTEM: "+oi.OS_system+"\n"+"OS_VERSION: "+oi.OS_version+"\n"+\
        "OS_KERNEL_VERSION: "+oi.OS_kernel_version+"\n"+"OS_HOSTNAME: "+oi.OS_hostname+"\n"+\
        "OS_MACHINE: "+oi.OS_machine+"\n"+"OS_PROCESSOR: "+oi.OS_processor+"\n"+\
        "OS_ARCHITECTURE: "+oi.OS_architecture+"\n"
    osinfo_writestr=str(time.strftime("%Y-%m-%d %X",time.localtime()))+"# osinfo\n"+osinfo_pre_writestr+"\n"

    #保存userinfo
    ou=bronze_os.OSusers()
    userinfo_pre_writestr="USERS: "+str(ou.baseinfo)+"\n"+"HOMEDIR: "+str(ou.homedir)+"\n"+\
        "SHELL: "+str(ou.shell)+"\n"+"PRIMEGROUP: "+str(ou.primegroup)+"\n"
    userinfo_writestr=str(time.strftime("%Y-%m-%d %X",time.localtime()))+"# userinfo\n"+userinfo_pre_writestr+"\n"

    #保存groupinfo
    og=bronze_os.OSgroups()
    groupinfo_pre_writestr="GROUPS: "+str(og.baseinfo)+"\n"+"MEMBERS: "+str(og.member)+"\n"
    groupinfo_writestr=str(time.strftime("%Y-%m-%d %X",time.localtime()))+"# groupinfo\n"+groupinfo_pre_writestr+"\n"

    writestr=osinfo_writestr+userinfo_writestr+groupinfo_writestr
    logdata=bronze_logdata.Logdata()
    logdata.set("osinfo",writestr)
    logdata.writelog()

    return

def __usage():
    usage_content=\
'''
usage osinfo.py [-hswl | --help --write --show <[osinfo]|[uid="ID"]|[uname=“NAME”]|[gid="ID"]|[gname="NAME"]|[uid_group="ID"]|[uname_group="NAME"]> --logfile path_name]

-h/--help 打印帮助信息
-w/--write 保存LOG文件
-s/--show 只显示信息，不保存
    osinfo 显示系统信息
    uid="ID" 显示指定用户ID信息
    uname=“NAME” 显示指定用户名信息
    gid="ID" 显示指定组ID信息
    gname="NAME" 显示指定组名信息
    uid_group="ID" 显示指定用户ID所有组信息
    uname_group="NAME" 显示指定用户名所有组信息
-l/-logfile = 指定日志存储位置, 未完成
'''
    print(usage_content)
    return

def __show_info(st):
    sst=st.split("=")
    if sst[0]=="osinfo":
        oi=bronze_os.OSinfo()
        osinfo_str="OS_SYSTEM: "+oi.OS_system+"\n"+"OS_VERSION: "+oi.OS_version+"\n"+\
            "OS_KERNEL_VERSION: "+oi.OS_kernel_version+"\n"+"OS_HOSTNAME: "+oi.OS_hostname+"\n"+\
            "OS_MACHINE: "+oi.OS_machine+"\n"+"OS_PROCESSOR: "+oi.OS_processor+"\n"+\
            "OS_ARCHITECTURE: "+oi.OS_architecture+"\n"
        print(osinfo_str)
    elif sst[0]=="uid":
        ui=bronze_os.user_info(uid=sst[1])
        print("uid=%s, username=%s, homedir=%s, shell=%s, prime_gid=%s" % \
              (ui[0],ui[1],ui[2],ui[3],ui[4]))
    elif sst[0]=="uname":
        ui=bronze_os.user_info(name=sst[1])
        print("uid=%s, username=%s, homedir=%s, shell=%s, prime_gid=%s" % \
              (ui[0],ui[1],ui[2],ui[3],ui[4]))
    elif sst[0]=="gid":
        gi=bronze_os.group_info(gid=sst[1])
        print("gid=%s, groupname=%s, member=%s" %\
              (gi[0],gi[1],gi[2]))
    elif sst[0]=="gname":
        gi=bronze_os.group_info(name=sst[1])
        print("gid=%s, groupname=%s, member=%s" %\
              (gi[0],gi[1],gi[2]))
    elif sst[0]=="uid_group":
        ug=bronze_os.user_group(uid=sst[1])
        print(ug)
    elif sst[0]=="uname_group":
        ug=bronze_os.user_group(name=sst[1])
        print(ug)
    else:
        print("wrong args!")
        __usage()
        exit()

    return

if __name__ == "__main__" :
    check_platform(PLATFORM) #监测运行平台是否符合要求
    main(sys.argv[1:])


