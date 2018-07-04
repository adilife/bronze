#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.

import time
import sys, getopt

#import bronze mod
import bronze_lib.bronze_dmi as dmi
import bronze_lib.bronze_logdata as logdata
from bronze_lib.bronze_common import *

#定义DMI TYPE
BIOS=[b"0,",b"13,"]
SYSTEM=[b"1,", b"12,", b"15,", b"23,", b"32,"]
BASEBOARD=[b"2,",b"10,"]
CHASSIS=[b"3,"]
PROCESSOR=[b"4,"]
MEMORY=[b"5,",b"6,",b"16,",b"17,"]
CACHE=[b"7,"]
CONNECTOR=[b"8,"]
SLOT=[b"9,"]
DETAIL_TYPE={'BIOS': b'0,', 'System': b'1,', 'Base Board': b'2,', 'Chassis': b'3,', \
         'Processor': b'4,', 'Memory Controller': b'5,', 'Memory Module': b'6,', \
         'Cache': b'7,', 'Port Connector': b'8,', 'System Slots': b'9,', 'On Board Devices': b'10,', \
         'OEM Strings': b'11,', 'System Configuration Options': b'12,', 'BIOS Language': b'13,', \
         'Group Associations': b'14,', 'System Event Log': b'15,', 'Physical Memory Array': b'16,', \
         'Memory Device': b'17,', '32-bit Memory Error': b'18,', 'Memory Array Mapped Address': b'19,', \
         'Memory Device Mapped Address': b'20,', 'Built-in Pointing Device': b'21,', 'Portable Battery': b'22,', \
         'System Reset': b'23,', 'Hardware Security': b'24,', 'System Power Controls': b'25,', 'Voltage Probe': b'26,', \
         'Cooling Device': b'27,', 'Temperature Probe': b'28,', 'Electrical Current Probe': b'29,', \
         'Out-of-band Remote Access': b'30,', 'Boot Integrity Services': b'31,', 'System Boot': b'32,', \
         '64-bit Memory Error': b'33,', 'Management Device': b'34,', 'Management Device Component': b'35,', \
         'Management Device Threshold Data': b'36,', 'Memory Channel': b'37,', 'IPMI Device': b'38,', \
         'Power Supply': b'39,'}

DMI_TYPE_CONTENT='''
TYPE Information
       Keyword     Types
       ------------------------------
       bios        0, 13
       system      1, 12, 15, 23, 32
       baseboard   2, 10
       chassis     3
       processor   4
       memory      5, 6, 16, 17
       cache       7
       connector   8
       slot        9
       
SubType   Information
       ----------------------------------------
          0   BIOS
          1   System
          2   Base Board
          3   Chassis
          4   Processor
          5   Memory Controller
          6   Memory Module
          7   Cache
          8   Port Connector
          9   System Slots
         10   On Board Devices
         11   OEM Strings
         12   System Configuration Options
         13   BIOS Language
         14   Group Associations
         15   System Event Log
         16   Physical Memory Array
         17   Memory Device
         18   32-bit Memory Error
         19   Memory Array Mapped Address
         20   Memory Device Mapped Address
         21   Built-in Pointing Device
         22   Portable Battery
         23   System Reset
         24   Hardware Security
         25   System Power Controls
         26   Voltage Probe
         27   Cooling Device
         28   Temperature Probe
         29   Electrical Current Probe
         30   Out-of-band Remote Access
         31   Boot Integrity Services
         32   System Boot
         33   64-bit Memory Error
         34   Management Device
         35   Management Device Component
         36   Management Device Threshold Data
         37   Memory Channel
         38   IPMI Device
         39   Power Supply
'''


def main(argv):
    log_file = ''
    show_argv = ''
    
    try:
        opts, args = getopt.getopt(argv,"ht:s:",["help","type=","subtype="])
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
            elif opt in ("-t", "--type"):
                print("type argv")
                __show_type(arg)
            elif opt in ("-s", "--subtype"):
                print("type argv")
                __show_subtype(arg)
    return

def __show_type(st):
    di=dmi.Dmi()
    dt=compile("di.parse_data(%s)" % st.upper(), "", "eval")
    try:
        m,n=eval(dt)
    except NameError as e:
        print("Wrong Type!")
        __usage()
        return

    for k,v in enumerate(m):
        try:
            print(k,v)
        except BrokenPipeError as e:
            return
        except KeyboardInterrupt as e:
            return
    return

def __show_subtype(st):
    di=dmi.Dmi()
    dt=(st+",").encode("ascii")
    m,n=di.parse_data(dt)
    for k,v in enumerate(m):
        try:
            print(k,v)
        except BrokenPipeError as e:
            return
        except KeyboardInterrupt as e:
            return
    return

def __usage():
    usage_content=\
'''
usage dmiinfo.py [-hts | --help --type=types --subtype=subtypes]

-h/--help 打印帮助信息
-t/--type 打印指定类型信息
-s/-subtype 打印指定子类信息
'''
    print(usage_content)
    print(DMI_TYPE_CONTENT)
    return

if __name__ == "__main__" :
    check_platform(PLATFORM) #监测运行平台是否符合要求
    main(sys.argv[1:])



