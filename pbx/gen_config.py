# -*- coding: utf-8 -*-
import os

from mole.template import jinja2_template

from models import Fs_Sipinterface,Fs_Context,Fs_Netlist,Fs_Location
from models import Fs_Number,Fs_Voicemail,Fs_Device,Fs_Ringgroup,Fs_Autoattendant,Fs_Conference,Fs_TimeRoutes,Fs_Trunk_Routepattern
import config
from openerp import tools
import mole

ADDONS_PATH = tools.config['addons_path'].split(",")[-1]#config.ADDONS_PATH
tpl_path = os.path.join(ADDONS_PATH,'oe_pbx', 'pbx', 'tpl')
print '>>>>>>>',tpl_path,mole.__file__
out_path = config.fs_conf_path

odbc_credentials = config.odbc_credentials

def sip_profiles():
    u'''
    sip_profiles
    '''
    profiles = Fs_Sipinterface.select()
    m_data = jinja2_template('sip_profiles',template_lookup=[tpl_path], profiles=profiles, odbc_credentials=odbc_credentials ) 
    m_file = os.path.join(out_path,'sip_profiles', 'oe_profiles.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()
    
def autoload_acl():
    u'''
    autoload_acl
    '''
    netlist = Fs_Netlist.select()
    m_data = jinja2_template('autoload_configs_acl',template_lookup=[tpl_path], netlist=netlist) 
    m_file = os.path.join(out_path,'autoload_configs', 'oe_acl.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()
    
def autoload_locations():
    u'''
    autoload_locations
    '''
    locations = Fs_Location.select()
    m_data = jinja2_template('autoload_configs_locations',template_lookup=[tpl_path], locations=locations) 
    m_file = os.path.join(out_path,'autoload_configs', 'oe_locations.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()
    
def autoload_conferences():
    u'''
    autoload_locations
    '''
    conferences = Fs_Conference.select()
    m_data = jinja2_template('autoload_configs_conference',template_lookup=[tpl_path], conferences=conferences) 
    m_file = os.path.join(out_path,'autoload_configs', 'oe_conferences.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()
    
def ivr_menus():
    u'''
    ivr_menus
    '''
    menus = Fs_Autoattendant.select()
    m_data = jinja2_template('ivr_menus',template_lookup=[tpl_path], menus=menus) 
    m_file = os.path.join(out_path,'ivr_menus', 'oe_ivr.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()
    
def directory():
    u'''
    directory
    '''
    locations = Fs_Location.select()
    voicemails = Fs_Voicemail.select()
    m_data = jinja2_template('directory',template_lookup=[tpl_path], locations=locations, voicemails=voicemails ) 
    m_file = os.path.join(out_path,'directory', 'oe_directory.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()
    
def dialplan():
    u'''
    dialplan
    '''
    contexts = {}
    trunkroutes = Fs_Trunk_Routepattern.select()
    for vm in trunkroutes:
        ct = vm.trunk.sipinterface.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("trunkroutes"):contexts[ct]["trunkroutes"]=[]
        contexts[ct]["trunkroutes"].append(vm)
    timeroutes = Fs_TimeRoutes.select()
    for vm in timeroutes:
        ct = vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("timeroutes"):contexts[ct]["timeroutes"]=[]
        contexts[ct]["timeroutes"].append(vm)
    voicemails = Fs_Voicemail.select()
    for vm in voicemails:
        ct = vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("voicemails"):contexts[ct]["voicemails"]=[]
        contexts[ct]["voicemails"].append(vm)
    devices = Fs_Device.select()
    for vm in devices:
        ct = vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("devices"):contexts[ct]["devices"]=[]
        contexts[ct]["devices"].append(vm)
    ringgroups = Fs_Ringgroup.select()
    for vm in ringgroups:
        ct = vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("ringgroups"):contexts[ct]["ringgroups"]=[]
        contexts[ct]["ringgroups"].append(vm)
    attendants = Fs_Autoattendant.select()
    for vm in attendants:
        ct = vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("attendants"):contexts[ct]["attendants"]=[]
        contexts[ct]["attendants"].append(vm)
    conferences = Fs_Conference.select()
    for vm in conferences:
        ct = vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("conferences"):contexts[ct]["conferences"]=[]
        contexts[ct]["conferences"].append(vm)
    all_context = Fs_Context.select()
    for vm in all_context:
        ct = vm.number.context.id
        if contexts.has_key[ct]:
            contexts[ct]['endtype'] = vm.endtype
            contexts[ct]['tts_string'] = vm.tts_string
            contexts[ct]['media_file'] = vm.media_file
    
    for context_id in contexts.keys():
        context = contexts[context_id]
        context["id"] = context_id
        m_data = jinja2_template('dialplan',template_lookup=[tpl_path], context=context) 
        m_file = os.path.join(out_path,'dialplan', 'oe_context_%s.xml'%context_id)
        f = open(m_file,'w+')
        f.write(m_data)
        f.close()
        
def main():
    sip_profiles()
    autoload_acl()
    autoload_locations()
    autoload_conferences()
    directory()
    dialplan()

if __name__=="__main__":
    main()

