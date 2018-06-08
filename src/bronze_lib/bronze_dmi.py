#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.

'''
class Dmi : 定义DMI类，DMI.dmi为从dmidecode命令读取的输入内容
class Bios  # 定义Bios类. 
    biosinfo # bios信息，元组
    
    system() #返回system信息
    baseboard() #返回baseboard信息
    chassis()  #返回chassis信息
    processor() #返回processor信息
    memory()  #返回memory信息
    cache()  #返回cache信息
    connector()  #返回connector信息
    slot()  #返回slot信息
    

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
DETAIL_TYPE={'0': 'BIOS', '1': 'System', '2': 'Base Board', '3': 'Chassis', \
         '4': 'Processor', '5': 'Memory Controller', '6': 'Memory Module', \
         '7': 'Cache', '8': 'Port Connector', '9': 'System Slots', '10': 'On Board Devices', \
         '11': 'OEM Strings', '12': 'System Configuration Options', '13': 'BIOS Language', \
         '14': 'Group Associations', '15': 'System Event Log', '16': 'Physical Memory Array', \
         '17': 'Memory Device', '18': '32-bit Memory Error', '19': 'Memory Array Mapped Address', \
         '20': 'Memory Device Mapped Address', '21': 'Built-in Pointing Device', '22': 'Portable Battery', \
         '23': 'System Reset', '24': 'Hardware Security', '25': 'System Power Controls', '26': 'Voltage Probe', \
         '27': 'Cooling Device', '28': 'Temperature Probe', '29': 'Electrical Current Probe', \
         '30': 'Out-of-band Remote Access', '31': 'Boot Integrity Services', '32': 'System Boot', \
         '33': '64-bit Memory Error', '34': 'Management Device', '35': 'Management Device Component', \
         '36': 'Management Device Threshold Data', '37': 'Memory Channel', '38': 'IPMI Device', \
         '39': 'Power Supply'}

class Dmi(object):

    def __init__(self):
        self.dmi=()
        
        self.__get()
        return
    
    def __get(self):
        self.dmi=self.__get_dmidecode()
        return
    
    def __get_dmidecode(self):
        data=[]
        p = Popen('dmidecode',shell=True,stdout=PIPE, stderr=PIPE).stdout.read().split(b"\n")
        return tuple(p)


class Bios(object):
    def __init__(self):
        self.biosinfo = ()
        self.__bios=()

        self.__get()
        return

    def __get(self):
        self.__get_baseinfo()
        return

    def __get_baseinfo(self):
        dmidata=Dmi().dmi
        bindata,strdata=parse_data(dmidata, BIOS)
        
        self.biosinfo=strdata
        self.__bios=bindata
        return 

class system(object):
        pass
        
    
class baseboard(object):
        pass
        
class chassis(object):
        pass
        
    
class processor(object):
        pass
        
    
class Memory(object):
    def __init__(self):
        self.meminfo = ()
        self.__mem=()

        self.__get()
        return

    def __get(self):
        self.__get_baseinfo()
        self.__get_memctrl()
        return

    def __get_baseinfo(self):
        dmidata=Dmi().dmi
        bindata,strdata=parse_data(dmidata, MEMORY)
        
        self.meminfo=strdata
        self.__mem=bindata
        return 
    
    #未完成
    def __get_memctrl(self):
        dmidata=Dmi().dmi
        bindata,strdata=parse_data(dmidata, [b"5,"])
        print(bindata)
        for k,v in enumerate(strdata):
            print(k,v)
        return
        
    
class cache(object):
        pass
        
    
class connector(object):
        pass
        
    
class slot(object):
        pass
        

def parse_data(dmidata,dmitype):
    tmp_parse=[]
    istype=False
    for id,line  in enumerate(dmidata) :
        tmp_data=line.split(b" ")
        if tmp_data[0] == b"Handle" and tmp_data[4] in dmitype:
            #print(tmp_data)
            istype=True
        
        if istype:
            if tmp_data[0] == b"" :
                istype = False
            else :
                tmp_parse.append(line)
    
    str_tmp_parse=[]
    for k,v in enumerate(tmp_parse):
        str_tmp_parse.append(v.decode("ascii"))
    return tuple(tmp_parse),tuple(str_tmp_parse)


    
a=Memory()






