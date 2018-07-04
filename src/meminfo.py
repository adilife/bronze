#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.

import time
import sys, getopt

#import bronze mod
import bronze_lib.bronze_mem
import bronze_lib.bronze_logdata
import bronze_lib.bronze_dmi as dmi
from bronze_lib.bronze_common import *

MEM_DMI_DETAIL=\
'''
          5   Memory Controller
          6   Memory Module
         16   Physical Memory Array
         17   Memory Device
         18   32-bit Memory Error
         19   Memory Array Mapped Address
         20   Memory Device Mapped Address
         37   Memory Channel
'''

MEM_DMI_TYPE=\
'''
       memory      5, 6, 16, 17
'''


def main(argv):
    log_file = ''
    show_argv = ''
    
    try:
        opts, args = getopt.getopt(argv,"hkmgswl:d",["help","write","show","logfile=","dev"])
    except getopt.GetoptError:
        print("wrong args!")
        __usage()
        exit()

    #命令行无参数处理
    if opts==[] :
        print("no args!")
        __show_info("s")
        exit()
    else:
        #命令行参数处理
        for opt, arg in opts:
            if opt == "--help":
                __usage()
                exit()
            elif opt in ("-w", "--write"):
                print("write argv")
                __write_log()
            elif opt in ("-s", "--show"):
                __show_info("s")
                exit()
            elif opt in ("-l", "--logfile"):
                log_file = arg
                print("logfile")
            elif opt in ("-d", "--dev"):
                __show_dev()
            elif opt == "-h":
                __show_info("h")
                exit()
            elif opt == "-k":
                __show_info("k")
                exit()
            elif opt == "-m":
                __show_info("m")
                exit()
            elif opt == "-g":
                __show_info("g")
                exit()

    return


def __usage():
    usage_content=\
'''
usage meminfo.py [-hkmgswld | --help --write --show --logfile=path_name --dev=devname]

--help 打印帮助信息
-h 人类友好信息显示
-k KB为单位显示
-m MB为单位显示
-g GB为单位显示
-w/--write 保存LOG文件
无参数/-s/--show 只显示信息，不保存
-l/--logfile = 指定日志存储位置, 未完成
-d/--dev 显示内存硬件信息
'''
    print(usage_content)
    return

def __show_info(st):
    #define GB & MB, default data is KB
    MB=1024
    GB=1024*1024

    prt_str=""
    mi=bronze_lib.bronze_mem.Mem()

    if st == "h" :
        #show in human friendly
        tmp_num=0
        prt_num=0
        ht=""
        for k,v in enumerate(mi.allinfo):
            tmp_num=int(v[1])
            if GB > tmp_num > MB:
                prt_num = round(tmp_num/MB,2)
                ht="MB"
            elif tmp_num > GB:
                prt_num = round(tmp_num/GB,2)
                ht="GB"
            else:
                prt_num = tmp_num
                ht="KB"
            #print("%s = %s %s" % (v[0],str(prt_num),ht))
            print("{:13s} =  {} {}".format(v[0],str(prt_num),ht))
    elif st in ["k","s"] :
        #show in KB, default data is KB
        mi.print_info()
    elif st == "m" :
        #show in MB, default data is KB
        for k,v in enumerate(mi.allinfo):
            print("{:13s} =  {} MB".format(v[0],str(round(int(v[1])/MB))))
    elif st == "g" :
        #show in GB, default data is KB
        for k,v in enumerate(mi.allinfo):
            print("{:13s} =  {} GB".format(v[0],str(round(int(v[1])/GB))))    

    return

def __write_log():
    #保存meminfo
    mi=bronze_lib.bronze_mem.Mem()
    mi_pre_writestr=""
    for k,v in enumerate(mi.allinfo):
        mi_pre_writestr += "{:12s} =  {}\n".format(v[0],v[1])

    writestr=str(time.strftime("%Y-%m-%d %X",time.localtime()))+"# meminfo\n"+mi_pre_writestr+"\n"
    logdata=bronze_lib.bronze_logdata.Logdata()
    logdata.set("meminfo",writestr)
    logdata.writelog()

    return

def __show_dev():
    print("show dev")
    dv=dmi.Dmi()
    controller,bin_controller=dv.parse_data(dmi.DETAIL_TYPE['Memory Controller'])
    module,bin_module=dv.parse_data(dmi.DETAIL_TYPE['Memory Module'])
    controller_data=__parse_mem_controller(controller)
    module_data=__parse_mem_module(module)
    
    #print Controller data
    print("\nMemory Controller Info:")
    for k,v in enumerate(controller_data):
        print("{:27s}: {}".format(v[0],v[1]))

    #print Module data
    print("\nMemory Module Info:")
    flag_stop=False
    prt_str_l1=""
    prt_str_l2=""
    prt_str=""
    for k,v in enumerate(module_data):
        for k,v in enumerate(v):
            if v[0] == 'Socket Designation':
                #print("{}{}:".format(v[0],v[1]))
                prt_str_l1 += "{}{}:\n".format(v[0],v[1])
            else:
                #print("{:20s}:{}".format(v[0],v[1]))
                prt_str_l2 += "{:27s}: {}\n".format(v[0],v[1])
                if v[1]=='Not Installed':
                    flag_stop=True
                    prt_str_l1=''
                    prt_str_l2=''
                    break
        if flag_stop:
            break
        else :
            prt_str += prt_str_l1 + prt_str_l2
            prt_str_l1=""
            prt_str_l2=""
    print(prt_str)
    return

def __parse_mem_module(module):
    module_data=[]
    module_template=['Socket Designation', 'Current Speed', 'Type', 'Installed Size', 'Enabled Size', 'Error Status']
    tmp_parse=[]
    islevel1=False
    islevel2=False
    flag_append=0
    for id,line in enumerate(module):
        if line.startswith("\t"):
            islevel2 = True
            islevel1 = False
        else :
            islevel1 = True
            islevel2 = False

        if islevel1 :
            flag_append += 1

        if  flag_append == 2:
            module_data.append(tuple(tmp_parse))
            flag_append = 0
            tmp_parse=[]
        
        if islevel2 :
            tmp_str=line.strip().split(": ")
            tmp_parse.append(tuple(tmp_str))
        
    module_data.pop(0)
    return tuple(tuple(module_data))

def __parse_mem_controller(controller):
    controller_data=[]
    tmp_parse=[]
    controller_template=['Supported Interleave', 'Current Interleave', \
                         'Maximum Memory Module Size', 'Maximum Total Memory Size', \
                         'Memory Module Voltage', 'Associated Memory Slots']

    for id,line in enumerate(controller):
        if line.startswith("\t\t"):
            continue
        elif line.startswith("\t"):
            tmp_parse.append(line.strip().split(": "))
        else:
            continue

    for k,v in enumerate(tmp_parse):
        if v[0] in controller_template:
            controller_data.append((v[0],v[1]))

    return tuple(controller_data)



if __name__ == "__main__" :
    check_platform(PLATFORM) #监测运行平台是否符合要求
    main(sys.argv[1:])


