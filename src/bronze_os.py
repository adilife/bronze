#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.

'''
class OSinfo: OS_version, OS_kernel_version, OS_hostname, OS_system, OS_architecture, OS_machine, OS_processor
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
        return
    
    def __get_osinfo(self):
        tmp_osinfo=platform.uname()
        self.OS_system=tmp_osinfo[0]
        self.OS_hostname=tmp_osinfo[1]
        self.OS_kernel_version=tmp_osinfo[2]
        self.OS_version=tmp_osinfo[3][1:]
        self.OS_machine=tmp_osinfo[4]
        self.OS_processor=tmp_osinfo[5]
        self.OS_architecture=str(platform.architecture())
        return

    def print_info(self):
        print("OS_SYSTEM: %s \nOS_VERSION: %s \nOS_KERNEL_VERSION: %s \nOS_HOSTNAME: %s" \
              % (self.OS_system,self.OS_version,self.OS_kernel_version,self.OS_hostname))
        print("OS_MACHINE: %s \nOS_PROCESSOR: %s \nOS_ARCHITECTURE: %s \n" \
              %(self.OS_machine,self.OS_processor,self.OS_architecture))
        return


class OSusers(object):
    def __init__(self):
        self.baseinfo={}
        self.homedir={}
        self.shell={}
        self.primegroup={}
        
        self.__get()
    
    def __get(self):
        self.__get_info()
        
        return
        
    def __get_info(self):
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
        print()
        return


class OSgroups(object):
    def __init__(self):
        self.baseinfo={}
        self.member={}
        
        self.__get()
    
    def __get(self):
        self.__get_info()
        return

    def __get_info(self):
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
        print()
        return

def group_info(gid="", name=""):
    us=OSusers()
    gs=OSgroups()
    ginfo=("",)
    tmp_name=""
    tmp_member=""
    tmp_gid=""
    if gid != "" and name == "":
        try:
            tmp_name=gs.baseinfo[gid]
        except:
            pass
        try:
            tmp_member=gs.member[gid]
        except:
            pass
        
        tmp_gid=gid
        
    elif gid == "" and name != "":
        tmp_gid=gid
        for tt in enumerate(gs.baseinfo.items()):
            if tt[1][1] == name:
                tmp_gid=tt[1][0]
                tmp_name=name

        try:
            tmp_member=gs.member[tmp_gid]
        except:
            pass
        
    elif gid == "" and name == "":
        pass
    
    else :
        tmp_name=name
        tmp_gid=gid
        if tmp_name != gs.baseinfo[gid]:
            tmp_name=""
            tmp_gid=""
            tmp_member=""
        else:
            for tt in enumerate(us.baseinfo.items()):
                if tmp_name == tt[1][1]:
                    if tmp_member != "":
                        tmp_member=tmp_name+","+tmp_member
                    tmp_member=tmp_name

    ginfo=(tmp_gid,tmp_name,tmp_member)
    return ginfo

#返回给定用户的组信息, return (("gid","gname"),)
def user_group(uid="",name=""):
    gids=[]
    tmp_gids=[]
    tmp_name=""
    tmp_uid=""
    us=OSusers()
    gs=OSgroups()
    
    if uid != "" and name == "" :
        for tt in enumerate(us.baseinfo.items()):
            if uid == tt[1][0]:
                tmp_name=tt[1][1]
        if tmp_name != "":
            for tt in enumerate(gs.member.items()):
                if tmp_name in tt[1][1]:
                    tmp_gids.append(tt[1][0])
            for tg in enumerate(tmp_gids):
                tgn=gs.baseinfo[tg[1]]
                gids.append(tuple([tg[1],tgn]))
    
    elif uid == "" and name != "" :
        for tt in enumerate(us.baseinfo.items()):
            if name == tt[1][1]:
                tmp_name=name
        if tmp_name != "":
            for tt in enumerate(gs.member.items()):
                if tmp_name in tt[1][1]:
                    tmp_gids.append(tt[1][0])
            for tg in enumerate(tmp_gids):
                tgn=gs.baseinfo[tg[1]]
                gids.append(tuple([tg[1],tgn]))

    elif uid != "" and name != "" :
        for tt in enumerate(us.baseinfo.items()):
            if name == tt[1][1]:
                if uid == tt[1][0]:
                    tmp_name=name
        if tmp_name != "":
            for tt in enumerate(gs.member.items()):
                if tmp_name in tt[1][1]:
                    tmp_gids.append(tt[1][0])
            for tg in enumerate(tmp_gids):
                tgn=gs.baseinfo[tg[1]]
                gids.append(tuple([tg[1],tgn]))

    else :
        pass

    return tuple(gids)

# 返回用户信息,return (uid,name,homedir,shell,prime_group_id)
def user_info(uid="", name=""):
    tmp_uid=""
    tmp_name=""
    tmp_homedir=""
    tmp_shell=""
    tmp_prime_group_id=""
    uinfo=[]
    gs=OSgroups()
    us=OSusers()

    if uid=="" and name != "":
        for tt in enumerate(us.baseinfo.items()):
            if name == tt[1][1]:
                tmp_uid=tt[1][0]
                tmp_name=name
        try:
            tmp_homedir=us.homedir[tmp_uid]
        except:
            pass
        try:
            tmp_shell=us.shell[tmp_uid]
        except:
            pass           
        try:
            tmp_prime_group_id=us.primegroup[tmp_uid]
        except:
            pass           
    
    elif uid != "" and name == "":
        for tt in enumerate(us.baseinfo.items()):
            if uid == tt[1][0]:
                tmp_name=tt[1][1]
                tmp_uid=uid
        try:
            tmp_homedir=us.homedir[tmp_uid]
        except:
            pass
        try:
            tmp_shell=us.shell[tmp_uid]
        except:
            pass           
        try:
            tmp_prime_group_id=us.primegroup[tmp_uid]
        except:
            pass
            
    #参数全空
    elif uid == "" and name == "":
        pass
    else:
        for tt in enumerate(us.baseinfo.items()):
            if uid == tt[1][0]:
                if name == tt[1][1]:
                    tmp_name=name
                    tmp_uid=uid
        try:
            tmp_homedir=us.homedir[tmp_uid]
        except:
            pass
        try:
            tmp_shell=us.shell[tmp_uid]
        except:
            pass           
        try:
            tmp_prime_group_id=us.primegroup[tmp_uid]
        except:
            pass

    uinfo=[tmp_uid,tmp_name,tmp_homedir,tmp_shell,tmp_prime_group_id]
    return tuple(uinfo)




