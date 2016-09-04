# -*- coding: utf-8 -*-
import os

from mole.template import jinja2_template

from apps.base import models as base_models
from apps.funcs import models as funcs_models
import config
import mole

cur = os.path.realpath(os.path.dirname(__file__))
tpl_path = os.path.join(cur, 'tpl')
out_path = config.fs_conf_path

odbc_credentials = config.odbc_credentials

def sip_profiles():
    u'''
    sip_profiles
    '''
    profiles = base_models.SipInterface.objects.all()
    m_data = jinja2_template('sip_profiles.xml',template_lookup=[tpl_path], profiles=profiles, odbc_credentials=odbc_credentials ) 
    m_file = os.path.join(out_path,'sip_profiles', 'oe_profiles.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()
    
def autoload_acl():
    u'''
    autoload_acl
    '''
    netlist = base_models.Netlist.objects.all()
    m_data = jinja2_template('autoload_configs_acl.xml',template_lookup=[tpl_path], netlist=netlist) 
    m_file = os.path.join(out_path,'autoload_configs', 'oe_acl.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()
    
def autoload_locations():
    u'''
    autoload_locations
    '''
    locations = base_models.Location.objects.all()
    m_data = jinja2_template('autoload_configs_locations.xml',template_lookup=[tpl_path], locations=locations) 
    m_file = os.path.join(out_path,'autoload_configs', 'oe_locations.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()
    
def autoload_conferences():
    u'''
    autoload_locations
    '''
    conferences = funcs_models.Conference.objects.all()
    m_data = jinja2_template('autoload_configs_conference.xml',template_lookup=[tpl_path], conferences=conferences) 
    m_file = os.path.join(out_path,'autoload_configs', 'oe_conferences.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()
    
def ivr_menus():
    u'''
    ivr_menus
    '''
    menus = funcs_models.Autoattendant.objects.all()
    m_data = jinja2_template('ivr_menus.xml',template_lookup=[tpl_path], menus=menus) 
    m_file = os.path.join(out_path,'ivr_menus', 'oe_ivr.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()
    
def directory():
    u'''
    directory
    '''
    locations = base_models.Location.objects.all()
    voicemails = funcs_models.VoiceMail.objects.all()
    m_data = jinja2_template('directory.xml',template_lookup=[tpl_path], locations=locations, voicemails=voicemails ) 
    m_file = os.path.join(out_path,'directory', 'oe_directory.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()
    
def dialplan():
    u'''
    dialplan
    '''
    contexts = {}
    trunkroutes = base_models.TrunkRoutePattern.objects.all()
    for vm in trunkroutes:
        ct = vm.trunk.sip_interface.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("trunkroutes"):contexts[ct]["trunkroutes"]=[]
        contexts[ct]["trunkroutes"].append(vm)
    timeroutes = funcs_models.TimeRoutes.objects.all()
    for vm in timeroutes:
        ct = vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("timeroutes"):contexts[ct]["timeroutes"]=[]
        contexts[ct]["timeroutes"].append(vm)
    voicemails = funcs_models.VoiceMail.objects.all()
    for vm in voicemails:
        ct = vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("voicemails"):contexts[ct]["voicemails"]=[]
        contexts[ct]["voicemails"].append(vm)
    devices = funcs_models.Device.objects.all()
    for vm in devices:
        ct = vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("devices"):contexts[ct]["devices"]=[]
        contexts[ct]["devices"].append(vm)
    ringgroups = funcs_models.RingGroup.objects.all()
    for vm in ringgroups:
        ct = vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("ringgroups"):contexts[ct]["ringgroups"]=[]
        contexts[ct]["ringgroups"].append(vm)
    attendants = funcs_models.Autoattendant.objects.all()
    for vm in attendants:
        ct = vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("attendants"):contexts[ct]["attendants"]=[]
        contexts[ct]["attendants"].append(vm)
    conferences = funcs_models.Conference.objects.all()
    for vm in conferences:
        ct = vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("conferences"):contexts[ct]["conferences"]=[]
        contexts[ct]["conferences"].append(vm)
    all_context = base_models.Context.objects.all()
    for vm in all_context:
        ct = vm.id#vm.number.context.id
        if contexts.has_key(ct):
            contexts[ct]['endtype'] = vm.end_type
            contexts[ct]['tts_string'] = vm.tts_string
            contexts[ct]['media_file'] = vm.media_file
    
    for context_id in contexts.keys():
        context = contexts[context_id]
        context["id"] = context_id
        m_data = jinja2_template('dialplan.xml',template_lookup=[tpl_path], context=context) 
        m_file = os.path.join(out_path,'dialplan', 'oe_context_%s.xml'%context_id)
        f = open(m_file,'w+')
        f.write(m_data)
        f.close()
        
def main():
    sip_profiles()
    autoload_acl()
    autoload_locations()
    autoload_conferences()
    ivr_menus()
    directory()
    dialplan()

if __name__=="__main__":
    main()

