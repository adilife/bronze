#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This file is a part of project Bronze.

import time
import sys, getopt

#import bronze mod
from bronze_lib.bronze_common import *
import bronze_lib.bronze_logdata as logdata
import bronze_lib.bronze_net as net



def main(argv):
    log_file = ''
    show_argv = ''
    
    try:
        opts, args = getopt.getopt(argv,"hs:",["help","show="])
    except getopt.GetoptError:
        print("wrong args!")
        __usage()
        exit()

    #命令行无参数处理
    if opts==[] :
        print("no args!")
        __show_info()
        exit()
    else:
        #命令行参数处理
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                __usage()
                exit()
            elif opt in ("-s", "--show"):
                __show_info(arg)
                exit()
    return


def __usage():
    usage_content=\
'''
usage netinfo.py [-hs | --help --show <interface|utilization>]

--help 打印帮助信息
无参数/-s/--show 只显示信息，不保存
    interface  显示网卡信息
    utilization   显示流量信息
'''
    print(usage_content)
    return

def __show_info(st=""):
    util_content=\
'''PORT : {}
    Rx    : {}
    Tx    : {}
'''
    if st == "" or st.upper() == "INTERFACE" :
        __show_ifinifo()
    elif st.upper() == "UTILIZATION" :
        mynic=net.Net_card()
        for k,v in enumerate(mynic.utilization().items()):
            print(util_content.format(v[0],v[1][0],v[1][1]))
    return

def __show_ifinifo():
    
    mynic=net.Net_card()
    nic_content=\
'''
Nic  : {}
    Pci_addr : {}
    Vendor   : {}
    Model    : {}
    S_vendor : {}
    S_model  : {}
    Rev      : {}
'''
    ip_content=\
'''        IP      : 
            ip_addr  : {}
            net_mask : {}
'''
    port_content=\
'''    PORT  ： {}
{}        STATS   :
            isup     : {}
            duplex   : {}
            speed    : {} Mb/s
            mtu      : {} Bytes
        MAC     :
            mac_addr : {}
        PCI     :
            pci_addr : {}
'''
    for k,v in enumerate(mynic.nic_attr.items()):
        pci_addr=v[0]
        vendor=v[1][1][1]
        model=v[1][1][2]
        s_vendor=v[1][1][3]
        s_model=v[1][1][4]
        rev=v[1][2][2:]
        nic_name="%s %s" % (s_vendor,s_model)
        print(nic_content.format(nic_name,pci_addr,vendor,model,s_vendor,s_model,rev))
        for k1,v1 in enumerate(mynic.nic_mac.items()):
            if v[0] == v1[1][0]:
                port_name=v1[0]
                str_port_ip=""
                #处理IP地址，考虑多IP地址情况
                for k2,v2 in enumerate(mynic.nic_addr[port_name]):
                    port_ip_addr=""
                    port_net_mask=""
                    #ipv4 & ipv6 addr
                    if str(v2[0])=="AddressFamily.AF_INET" or str(v2[0])=="AddressFamily.AF_INET6":
                        port_ip_addr=v2[1]
                        port_net_mask=v2[2]
                        str_port_ip += ip_content.format(port_ip_addr,port_net_mask)
                #处理 nic stats
                port_stats=mynic.nic_stats[port_name]
                port_isup=port_stats[0]
                port_duplex=str(port_stats[1]).split(".")[1]
                port_speed=port_stats[2]
                port_mtu=port_stats[3]
                #处理nic mac
                port_mac=mynic.nic_mac[port_name][1]
                #处理PCI addr
                port_pci_addr=mynic.nic_mac[port_name][0]
                print(port_content.format(port_name,str_port_ip,port_isup,port_duplex,port_speed,port_mtu,port_mac,port_pci_addr))
    return


if __name__ == "__main__" :
    check_platform(PLATFORM) #监测运行平台是否符合要求
    main(sys.argv[1:])




