#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.

'''

class Dmi : 定义DMI类，DMI.dmi为从dmidecode命令读取的输入内容
    def parse_data(dmidata,dmitype) 处理Dmi().dmi抓取的数据，返回两个值，str,ascii


DMI类型定义
 Type   Information
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

'''

from subprocess import Popen, PIPE



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

class Dmi(object):

    def __init__(self):
        self.dmi=()

        self.__get()
        return
    
    def __get(self):
        self.dmi=self.__get_dmidecode()
        return
    
    def __get_dmidecode(self):
        p = Popen('dmidecode',shell=True,stdout=PIPE, stderr=PIPE).stdout.read().split(b"\n")
        return tuple(p)

    def parse_data(self,dmitype=""):
        #处理空类型，返回全部内容
        if dmitype == "" :
            tmp_parse=self.dmi
            str_tmp_parse=[]
            for k,v in enumerate(tmp_parse):
                str_tmp_parse.append(v.decode("ascii"))
            return tuple(tmp_parse),tuple(str_tmp_parse)

        #检测dmitype类型，统一修改类型为list
        di=[]
        if not isinstance(dmitype,list):
            di.append(dmitype)
            dmitype=di
            
        #按照类型定义处理数据
        tmp_parse=[]
        istype=False
        for id,line  in enumerate(self.dmi) :
            tmp_data=line.split(b" ")
            if tmp_data[0] == b"Handle" and tmp_data[4] in dmitype:
                #print(tmp_data)
                #print(dmitype)
                istype=True

            if istype:
                if tmp_data[0] == b"" :
                    istype = False
                else :
                    tmp_parse.append(line)
       
        str_tmp_parse=[]
        for k,v in enumerate(tmp_parse):
            str_tmp_parse.append(v.decode("ascii"))
        return tuple(str_tmp_parse),tuple(tmp_parse)


