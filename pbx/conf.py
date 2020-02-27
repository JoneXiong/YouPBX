# -*- coding: utf-8 -*-
import os

from jinja2 import Environment, FileSystemLoader

from apps.base import models as base_models
from apps.funcs import models as funcs_models


fs_conf_path = None
odbc_credentials = '' #config.odbc_credentials

cur = os.path.realpath(os.path.dirname(__file__))
tpl_path = os.path.join(cur, 'tpl')
env = Environment(loader=FileSystemLoader(tpl_path))

def jinja2_template(tpl, **args):
    template = env.get_template(tpl)
    return template.render(**args)

def sip_profiles(fs_conf_path):
    u'''
    生成 sip_profiles
    '''
    profiles = base_models.SipInterface.objects.order_by("-id")
    m_data = jinja2_template('sip_profiles.xml', profiles=profiles, odbc_credentials=odbc_credentials )
    m_file = os.path.join(fs_conf_path,'sip_profiles', 'oe_profiles.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()

def autoload_acl(fs_conf_path):
    u'''
    生成 autoload_acl
    '''
    netlist = base_models.Netlist.objects.all()
    m_data = jinja2_template('autoload_configs_acl.xml', netlist=netlist)
    m_file = os.path.join(fs_conf_path,'autoload_configs', 'oe_acl.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()

def autoload_locations(fs_conf_path):
    u'''
    生成 autoload_locations
    '''
    locations = base_models.Location.objects.all()
    m_data = jinja2_template('autoload_configs_locations.xml', locations=locations)
    m_file = os.path.join(fs_conf_path,'autoload_configs', 'oe_locations.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()

def autoload_conferences(fs_conf_path):
    u'''
    autoload_conferences
    '''
    conferences = funcs_models.Conference.objects.all()
    m_data = jinja2_template('autoload_configs_conference.xml', conferences=conferences)
    m_file = os.path.join(fs_conf_path,'autoload_configs', 'oe_conferences.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()

def ivr_menus(fs_conf_path):
    u'''
    ivr_menus
    '''
    from apps.extend.models import IVR
    menus = IVR.objects.all()
    m_data = jinja2_template('ivr_menus.xml', menus=menus)
    m_file = os.path.join(fs_conf_path,'ivr_menus', 'oe_ivr.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()

def directory(fs_conf_path):
    u'''
    directory
    '''
    locations = base_models.Location.objects.all()
    voicemails = funcs_models.VoiceMail.objects.all()
    m_data = jinja2_template('directory.xml', locations=locations, voicemails=voicemails )
    m_file = os.path.join(fs_conf_path,'directory', 'oe_directory.xml')
    f = open(m_file,'w+')
    f.write(m_data)
    f.close()

def dialplan(fs_conf_path):
    u'''
    dialplan
    '''
    contexts = {}
    trunkroutes = base_models.TrunkRoutePattern.objects.all()
    for vm in trunkroutes:
        ct = vm.trunk.context.id
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
    devices = funcs_models.Device.objects.order_by("id")
    for vm in devices:
        ct = vm.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("devices"):contexts[ct]["devices"]=[]
        contexts[ct]["devices"].append(vm)
    ringgroups = funcs_models.RingGroup.objects.all()
    for vm in ringgroups:
        ct = vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("ringgroups"):contexts[ct]["ringgroups"]=[]
        contexts[ct]["ringgroups"].append(vm)
#     attendants = funcs_models.Autoattendant.objects.all()
#     for vm in attendants:
#         ct = vm.number.context.id
#         if not contexts.has_key(ct):contexts[ct]={}
#         if not contexts[ct].has_key("attendants"):contexts[ct]["attendants"]=[]
#         contexts[ct]["attendants"].append(vm)
    conferences = funcs_models.Conference.objects.all()
    for vm in conferences:
        ct = vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("conferences"):contexts[ct]["conferences"]=[]
        contexts[ct]["conferences"].append(vm)
    all_context = base_models.Context.objects.all()
    for vm in all_context:
        ct = vm.id#vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        contexts[ct]['endtype'] = vm.end_type
        contexts[ct]['tts_string'] = vm.tts_string
        contexts[ct]['media_file'] = vm.media_file
    from apps.extend.models import Extension
    all_extens = Extension.objects.all()
    for exten in all_extens:
        ct = 1#vm.number.context.id
        if not contexts.has_key(ct):contexts[ct]={}
        if not contexts[ct].has_key("extensions"):contexts[ct]["extensions"]=[]
        contexts[ct]["extensions"].append(exten)

    for context_id in contexts.keys():
        context = contexts[context_id]
        context["id"] = context_id
        m_data = jinja2_template('dialplan.xml', context=context)
        m_file = os.path.join(fs_conf_path,'dialplan', 'oe_context_%s.xml'%context_id)
        f = open(m_file,'w+')
        f.write(m_data)
        f.close()

def gen_all(fs_conf_path):
    sip_profiles(fs_conf_path)
    autoload_acl(fs_conf_path)
    autoload_locations(fs_conf_path)
    autoload_conferences(fs_conf_path)
    ivr_menus(fs_conf_path)
    directory(fs_conf_path)
    dialplan(fs_conf_path)


if __name__=="__main__":
    gen_all(fs_conf_path)

