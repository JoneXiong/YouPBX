# -*- coding: utf-8 -*-
import os

def get_ip_list():
    '''
    获取本机Ip地址列表
    '''
    ips = os.popen("/sbin/ifconfig | grep 'inet' | awk '{print $2}'").read()
    ips = ips.split('\n')
    return [e.replace('addr:', '') for e in ips if e]


def get_sipinterface_default_ip_list():
    ret = []
    ip_list = get_ip_list()
    for ip in ip_list:
        if (not ip.startswith('127.0.0.1') ) and (not ip.startswith('169.254.') ):
            ret.append(ip)
    return ret
