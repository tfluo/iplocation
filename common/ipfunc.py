#coding: utf8

#########################################################################
'''
from common.ipfunc import ip_int, ip_comp,
from common.ipfunc import is_host, is_ip
from common.ipfunc import subnet_of, sort_iplist
'''
#########################################################################
__doc__ = """IP Tools"""

import sys, os
import ipaddress
import string
from datetime import datetime, timedelta
from ipip.city import City

def now():
    return datetime.utcnow() + timedelta(hours=8)

def ipstr(ip):
    if isinstance(ip, str):
        return ip
    elif isinstance(ip, bytes):
        return ip.decode('utf8')
    else:
        return None

def ip_int(ip):
    ip = ipstr(ip)
    if not ip:
        return None
    else:
        try:
            return ipaddress.ip_interface(ip)
        except:
            return None

is_host = lambda ip: False if not ip_int(ip) else ip_int(ip).hostmask._ip == 0

def ip_comp(ip1, ip2):
    ipaddr1 = ipaddress.ip_interface(ip1)
    ipaddr2 = ipaddress.ip_interface(ip2)
    if ipaddr1.version == ipaddr2.version:
        if ipaddr1 > ipaddr2:
            return 1
        elif ipaddr1 < ipaddr2:
            return -1
        elif ipaddr1.hostmask._ip > ipaddr2.hostmask._ip:
            return 1
        elif ipaddr1.hostmask._ip < ipaddr2.hostmask._ip:
            return -1
        else:
            return 0
    elif ipaddr1.version > ipaddr2.version:
        return 1
    else:
        return -1

def is_ip(ip, is_network=False):
    result = False
    try:
        ipaddr = ip_int(ip)
        if ipaddr and not ipaddr.is_multicast and ipaddr.is_global:
            result = is_network or is_host(ip)
    except:
        s = sys.exc_info()
        f = sys._getframe()
        print('%s - %s(%s)[%d]: %s' % (
            now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            f.f_code.co_filename.replace(os.getcwd(), ''),
            f.f_code.co_name, 
            s[2].tb_lineno,
            s[1])
        )
    return result

def subnet_of(ip, network):
    result = False
    ipaddr1 = ip_int(ip)
    ipaddr2 = ip_int(network)
    if not ipaddr1:
        return False
    if not ipaddr2:
        return False
    if ipaddr1.version != ipaddr2.version:
        return False
    return ipaddr1.network.subnet_of(ipaddr2.network)


def sort_iplist(iplist):
    iplist = list(set(iplist))
    return sorted(iplist, ip_comp)
