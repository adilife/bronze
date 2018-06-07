#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.

'''
class Mem : 
    MemTotal: 所有可用RAM大小 （即物理内存减去一些预留位和内核的二进制代码大小）
    MemFree: LowFree与HighFree的总和，被系统留着未使用的内存
    Buffers: 用来给文件做缓冲大小
    Cached: 被高速缓冲存储器（cache memory）用的内存的大小（等于 diskcache minus SwapCache ）.
    SwapCached:被高速缓冲存储器（cache memory）用的交换空间的大小。已经被交换出来的内存，但仍然被存放在swapfile中。用来在需要的时候很快的被替换而不需要再次打开I/O端口。
    Active: 在活跃使用中的缓冲或高速缓冲存储器页面文件的大小，除非非常必要否则不会被移作他用.
    Inactive: 在不经常使用中的缓冲或高速缓冲存储器页面文件的大小，可能被用于其他途径.
    SwapTotal: 交换空间的总大小
    SwapFree: 未被使用交换空间的大小
    Dirty: 等待被写回到磁盘的内存大小。 
    Writeback: 正在被写回到磁盘的内存大小。
    AnonPages: 未映射页的内存大小
    Mapped: 设备和文件等映射的大小。
    Slab: 内核数据结构缓存的大小，可以减少申请和释放内存带来的消耗。
    SReclaimable:可收回Slab的大小
    SUnreclaim: 不可收回Slab的大小（SUnreclaim+SReclaimable＝Slab）
    PageTables: 管理内存分页页面的索引表的大小。
    NFS_Unstable:不稳定页表的大小
    VmallocTotal: 可以vmalloc虚拟内存大小
    VmallocUsed: 已经被使用的虚拟内存大小。

    allinfo: ((obj:value),) #上述信息组成的元组
    print_info() #打印信息
    
'''


class Mem(object):
    MEMOBJLIST=["MemTotal","MemFree","Buffers","Cached","SwapCached",\
                "Active","Inactive","SwapTotal","SwapFree","Dirty",\
                "Writeback","AnonPages","Mapped","Slab","SReclaimable",\
                "SUnreclaim","PageTables","NFS_Unstable","VmallocTotal",\
                "VmallocUsed"]
    def __init__(self):
        self.MemTotal = ""
        self.MemFree = ""
        self.Buffers = ""
        self.Cached = ""
        self.SwapCached = ""
        self.Active = ""
        self.Inactive = ""
        self.SwapTotal = ""
        self.SwapFree = ""
        self.Dirty = ""
        self.Writeback = ""
        self.AnonPages = ""
        self.Mapped = ""
        self.Slab = ""
        self.SReclaimable = ""
        self.SUnreclaim = ""
        self.PageTables = ""
        self.NFS_Unstable = ""
        self.VmallocTotal = ""
        self.VmallocUsed = ""
        self.allinfo=()
        
        self.__get()
        return

    def __get(self):
        self.__get_meminfo()
        return

    def __get_meminfo(self):
        run_cmd=""
        mi={}
        with open(r'/proc/meminfo','tr',errors='ignore') as cf:
            tmp_str=""
            for line in cf:
                tmp_str=line.split(":")
                mi[tmp_str[0]]=tmp_str[1].strip().split(" ")[0]
            cf.close()
        #处理字典内不需要的项目
        nmi={}
        for k,v in enumerate(mi.items()):
            for kk,vv in enumerate(self.MEMOBJLIST):
                if v[0] == vv :
                    nmi[v[0]]=v[1]
        mi=nmi
        #给属性赋值
        for k,v in enumerate(mi.items()):
            run_cmd += "self."+v[0]+" = "+v[1]+"\n"
        exec(compile(run_cmd,"","exec"))
        
        #self.allinfo
        i=0
        tmp_allinfo=[]
        for k,v in enumerate(mi.items()):
            if v[0] == self.MEMOBJLIST[i]:
                tmp_allinfo.append((v[0],v[1]))
                i+=1
        self.allinfo=tuple(tmp_allinfo)
        return 

    def print_info(self):
        for k,v in enumerate(self.allinfo):
            print("{:13s} =  {} KB".format(v[0],v[1]))
        return


