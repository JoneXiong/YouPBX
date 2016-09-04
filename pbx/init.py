# -*- coding: utf-8 -*-
import os
import shutil

from apps.base.models import SipInterface, Location
import config 

fs_conf_path = config.fs_conf_path


def get_ip_list():
    ips = os.popen("/sbin/ifconfig | grep 'inet addr' | awk '{print $2}'").read()
    ips = ips.split('\n')
    return [e.replace('addr:', '') for e in ips if e]

def create_sipinterface_with_ip(ip):
    # Authenticated
    obj = SipInterface()
    obj.name = 'Authenticated SIP on %s'%ip
    obj.ip_address = ip
    obj.sip_port = 5060
    obj.nat_net_listi_id = 2
    obj.inbound_net_list_id = 5
    obj.context = 2 # Publicly Accessible
    obj.auth = True
    # ...
    obj.save()
    # Unauthenticated
    obj = SipInterface()
    obj.name = 'Unauthenticated SIP on %s'%ip
    obj.ip_address = ip
    obj.sip_port = 5080
    obj.nat_net_list = 2
    obj.context = 2 # Publicly Accessible
    obj.auth = False
    # ...
    obj.save()
    
def get_sipinterface_default_ip_list():
    ret = []
    ip_list = get_ip_list()
    for ip in ip_list:
        if (not ip.startswith('127.0.0.1') ) and (not ip.startswith('169.254.') ):
            ret.append(ip)
    return ret

def create_default_Sipinterface():
    # generate default sip_profiles
    ip_list = get_ip_list()
    for ip in ip_list:
        if (not ip.startswith('127.0.0.1') ) and (not ip.startswith('169.254.') ):
            # Authenticated
            obj = SipInterface()
            obj.name = 'Authenticated SIP on %s'%ip
            obj.ip_address = ip
            obj.sip_port = 5060
            obj.nat_net_listi_id = 2
            obj.inbound_net_list_id = 5
            obj.context = 2 # Publicly Accessible
            obj.auth = True
            # ...
            obj.save()
            # Unauthenticated
            obj = SipInterface()
            obj.name = 'Unauthenticated SIP on %s'%ip
            obj.ip_address = ip
            obj.sip_port = 5080
            obj.nat_net_list = 2
            obj.context = 2 # Publicly Accessible
            obj.auth = False
            # ...
            obj.save()
    
def create_default_location():
    # generate default location
    import socket
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    obj = Location()
    obj.location_name = u'主区域'
    obj.domain_name = myaddr
    obj.save()

def xml_init():
    u'''
    delete sip_profiles root file; delete directory default.xml; 
    delete autoload_configs conference.conf.xml and acl.conf.xml
    add autoload_configs locations.conf.xml and odbc.conf.xml
    add sip_profiles  oe_sipinterfaces.xml
    '''
    #sip_profiles  init 
    sip_profiles_path = os.path.join(fs_conf_path, 'sip_profiles')
    bak_path = os.path.join(sip_profiles_path, 'bak')
    if not os.path.exists(bak_path):
        os.mkdir(bak_path)
    for e in os.listdir(sip_profiles_path):
        m_path = os.path.join(sip_profiles_path,e)
        if os.path.isfile(m_path):
            shutil.move(m_path, bak_path)
    #directory  init 
    sip_profiles_path = os.path.join(fs_conf_path, 'directory')
    bak_path = os.path.join(sip_profiles_path, 'bak')
    if not os.path.exists(bak_path):
        os.mkdir(bak_path)
    m_path = os.path.join(sip_profiles_path,'default.xml')
    shutil.move(m_path, bak_path)
    
    # autoload_configs init
    sip_profiles_path = os.path.join(fs_conf_path, 'autoload_configs')
    bak_path = os.path.join(sip_profiles_path, 'bak')
    if not os.path.exists(bak_path):
        os.mkdir(bak_path)
    m_path = os.path.join(sip_profiles_path,'conference.conf.xml')
    shutil.move(m_path, bak_path)
    m_path_acl = os.path.join(sip_profiles_path,'acl.conf.xml')
    shutil.move(m_path_acl, bak_path)
    
def main():
    xml_init()
    
if __name__=="__main__":
    main()
