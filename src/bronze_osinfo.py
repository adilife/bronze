#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.

'''
class OSusers: baseinfo{"uid":"name"}, homedir{"uid":"homedir"}, shell{"uid":"shell"}, primegroup{"uid":"gid"}
        __get() #初始化信息

        print_info() #打印信息

class OSgroups: baseinfo{"gid":"name"}, member{"uid":"member"}
        __get() #初始化信息

        print_info() #打印信息

user_info(uid="",name="") # 返回用户信息,return (uid,name,homedir,shell,prime_group_id)
group_info(gid="",name="") #返回组信息, return (gid,name,members)
user_group(uid="") #返回给定用户的组信息, return (("gid","gname"),)

'''


import platform

class OSinfo(object):
    def __init__(self):
        self.OS_version=""
        self.OS_kernel_version=""
        self.OS_hostname=""
        self.OS_system=""
        self.OS_architecture=""
        self.OS_machine=""
        self.OS_processor=""
        
        self.__get()

    def __get(self):
        self.__get_osinfo()
        self.__get_userinfo()
        return
    
    def __get_osinfo(self):
        tmp_osinfo=platform.uname()
        self.OS_system=tmp_osinfo[0]
        self.OS_hostname=tmp_osinfo[1]
        self.OS_kernel_version=tmp_osinfo[2]
        self.OS_version=tmp_osinfo[3]
        self.OS_machine=tmp_osinfo[4]
        self.OS_processor=tmp_osinfo[5]
        self.OS_architecture=platform.architecture()
        return
    
    def __get_userinfo(self):
        __sysstr = platform.system()
        if __sysstr == "Linux":
            self.__get_linux_userinfo()

        return
    
    def __get_linux_userinfo(self):
        pass
        return
    
    def print_info(self):
        print(" OS_SYSTEM: %s \n OS_VERSION: %s \n OS_KERNEL_VERSION: %s \n OS_HOSTNAME: %s \n" \
              % (a.OS_system,a.OS_version,a.OS_kernel_version,a.OS_hostname))
        print(" OS_MACHINE: %s \n OS_PROCESSOR: %s \n OS_ARCHITECTURE: %s \n" \
              %(a.OS_machine,a.OS_processor,a.OS_architecture))
        return


class OSusers(object):
    def __init__(self):
        self.baseinfo={}
        self.homedir={}
        self.shell={}
        self.primegroup={}
        
        self.__get()
    
    def __get(self):
        __sysstr = platform.system()
        if __sysstr == "Linux":
            self.__get_linux_info()
        
        return
        
    def __get_linux_info(self):
        with open(r'/etc/passwd','tr',errors='ignore') as cf:
            fc=[]
            for line in cf:
                fc=line.split(":")
                fc[-1]=fc[-1][:-1]
                self.baseinfo[fc[2]]=fc[0]
                self.homedir[fc[2]]=fc[5]
                self.shell[fc[2]]=fc[6]
                self.primegroup[fc[2]]=fc[3]
            cf.close()
        
        return
    
  
    def print_info(self):
        print("USERS: %s" % self.baseinfo)
        print("HOMEDIR: %s" % self.homedir)
        print("SHELL: %s" % self.shell)
        print("PRIMEGROUP: %s" % self.primegroup)
        
        return


class OSgroups(object):
    def __init__(self):
        self.baseinfo={}
        self.member={}
        
        self.__get()
    
    def __get(self):
        __sysstr = platform.system()
        if __sysstr == "Linux":
            self.__get_linux_info()
        return

    def __get_linux_info(self):
        with open(r'/etc/group','tr',errors='ignore') as cf:
            fc=[]
            us=OSusers()
            for line in cf:
                fc=line.split(":")
                fc[-1]=fc[-1][:-1]
                self.baseinfo[fc[2]]=fc[0]
                #生成member，如果/etc/group里member字段为“”，则member为gid=primegid对应的用户
                if fc[3] == "":
                    for tt in enumerate(us.primegroup.items()):
                        if fc[2] == tt[1][1]:
                            self.member[fc[2]]=us.baseinfo[tt[1][0]]
                else:
                    self.member[fc[2]]=fc[3]
            cf.close()
            
        return
    

    def print_info(self):
        print("GROUPS: %s" % self.baseinfo)
        print("MEMBERS: %s" % self.member)
        return

def user_info(self,uid="", name=""):
    pass
    return

#未测试
def group_info(gid="", name=""):
    us=OSusers()
    gs=OSgroups()
    ginfo=("",)
    if gid != "" and name == "":
        tmp_name=gs.baseinfo[gid]
        tmp_member=gs.member[gid]
        tmp_gid=gid

    if gid == "" and name != "":
        tmp_gid=""
        for tt in enumerate(gs.baseinfo.items()):
            if tt[1][1] == name:
                tmp_gid=tt[1][0]
        tmp_member=gs.member[tmp_gid]
        tmp_name=name
    
    for tt in enumerate(us.baseinfo.items()):
        if tmp_name == tt[1][1]:
            if tmp_member != "":
                tmp_member=tmp_name+","+tmp_member
            tmp_member=tmp_name
    ginfo=(tmp_gid,tmp_name,tmp_member)
    
    return ginfo

def user_group(uid=""):
    gids=[]
    tmp_gids=[]
    user_name=""
    us=OSusers()
    gs=OSgroups()
    if uid!="":
        for tt in enumerate(us.baseinfo.items()):
            if uid == tt[1][0]:
                user_name=tt[1][1]
        for tt in enumerate(gs.member.items()):
            if user_name in tt[1][1]:
                tmp_gids.append(tt[1][0])
        for tg in enumerate(tmp_gids):
            tgn=gs.baseinfo[tg[1]]
            gids.append(tuple([tg[1],tgn]))

    return tuple(gids)



a=OSinfo()
a.print_info()
b=OSusers()
b.print_info()
c=OSgroups()
c.print_info()

print(user_group("1000"))
