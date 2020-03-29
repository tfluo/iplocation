#coding: utf8

#########################################################################
'''
from common.iplocation import get_location
'''
#########################################################################

import os
from ipip.city import City
from common.ipfunc import ip_int

dbname = os.path.abspath('ipip/ipipfree.ipdb')
db = City(dbname)

def get_ipip_loc(ipaddr):
    if not ipaddr:
        ipipvalue = [''] * 3
    elif ipaddr.version == 6:
        ipipvalue = [''] * 3
    else:
        ipipvalue = db.find(str(ipaddr.ip), 'CN')
    return ipipvalue


def get_location(ip):
    ipaddr = ip_int(ip)
    ipipvalue = get_ipip_loc(ipaddr)
    
    data = {}
    data['ipip'] = ipipvalue

    return data


