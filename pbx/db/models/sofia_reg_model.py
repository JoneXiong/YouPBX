# -*- coding: utf-8 -*-

from peewee import *

import config

database = SqliteDatabase(config.fs_db_path+'sofia_reg_sipinterface_1.db', check_same_thread=False, **{})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class SipAuthentication(BaseModel):
    u'''
    会话验证数据
    '''
    expires = IntegerField(null=True)
    hostname = CharField(max_length=255, null=True)
    last_nc = IntegerField(null=True)
    nonce = CharField(max_length=255, null=True)
    profile_name = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'sip_authentication'

class SipDialogs(BaseModel):
    call = CharField(db_column='call_id', max_length=255, null=True)
    call_info = CharField(max_length=255, null=True)
    call_info_state = CharField(max_length=255, null=True)
    contact = CharField(max_length=255, null=True)
    contact_host = CharField(max_length=255, null=True)
    contact_user = CharField(max_length=255, null=True)
    direction = CharField(max_length=255, null=True)
    expires = IntegerField(null=True)
    hostname = CharField(max_length=255, null=True)
    presence_data = CharField(max_length=255, null=True)
    presence = CharField(db_column='presence_id', max_length=255, null=True)
    profile_name = CharField(max_length=255, null=True)
    rcd = IntegerField()
    rpid = CharField(max_length=255, null=True)
    sip_from_host = CharField(max_length=255, null=True)
    sip_from_tag = CharField(max_length=255, null=True)
    sip_from_user = CharField(max_length=255, null=True)
    sip_to_host = CharField(max_length=255, null=True)
    sip_to_tag = CharField(max_length=255, null=True)
    sip_to_user = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    status = CharField(max_length=255, null=True)
    user_agent = CharField(max_length=255, null=True)
    uuid = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'sip_dialogs'

class SipPresence(BaseModel):
    expires = IntegerField(null=True)
    hostname = CharField(max_length=255, null=True)
    network_ip = CharField(max_length=255, null=True)
    network_port = CharField(max_length=6, null=True)
    open_closed = CharField(max_length=255, null=True)
    profile_name = CharField(max_length=255, null=True)
    rpid = CharField(max_length=255, null=True)
    sip_host = CharField(max_length=255, null=True)
    sip_user = CharField(max_length=255, null=True)
    status = CharField(max_length=255, null=True)
    user_agent = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'sip_presence'

class SipRegistrations(BaseModel):
    u'''
    当前注册的用户
    '''
    call = CharField(db_column='call_id', max_length=255, null=True)
    contact = CharField(max_length=1024, null=True)
    expires = IntegerField(null=True)
    hostname = CharField(max_length=255, null=True)
    mwi_host = CharField(max_length=255, null=True)
    mwi_user = CharField(max_length=255, null=True)
    network_ip = CharField(max_length=255, null=True)
    network_port = CharField(max_length=6, null=True)
    orig_hostname = CharField(max_length=255, null=True)
    orig_server_host = CharField(max_length=255, null=True)
    presence_hosts = CharField(max_length=255, null=True)
    profile_name = CharField(max_length=255, null=True)
    rpid = CharField(max_length=255, null=True)
    server_host = CharField(max_length=255, null=True)
    server_user = CharField(max_length=255, null=True)
    sip_host = CharField(max_length=255, null=True)
    sip_realm = CharField(max_length=255, null=True)
    sip_user = CharField(max_length=255, null=True)
    sip_username = CharField(max_length=255, null=True)
    status = CharField(max_length=255, null=True)
    sub_host = CharField(max_length=255, null=True)
    user_agent = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'sip_registrations'

class SipSharedAppearanceDialogs(BaseModel):
    call = CharField(db_column='call_id', max_length=255, null=True)
    contact_str = CharField(max_length=255, null=True)
    expires = IntegerField(null=True)
    hostname = CharField(max_length=255, null=True)
    network_ip = CharField(max_length=255, null=True)
    profile_name = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'sip_shared_appearance_dialogs'

class SipSharedAppearanceSubscriptions(BaseModel):
    aor = CharField(max_length=255, null=True)
    call = CharField(db_column='call_id', max_length=255, null=True)
    contact_str = CharField(max_length=255, null=True)
    hostname = CharField(max_length=255, null=True)
    network_ip = CharField(max_length=255, null=True)
    profile_name = CharField(max_length=255, null=True)
    subscriber = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'sip_shared_appearance_subscriptions'

class SipSubscriptions(BaseModel):
    u'''
    注册脚本
    '''
    accept = CharField(max_length=255, null=True)
    call = CharField(db_column='call_id', max_length=255, null=True)
    contact = CharField(max_length=1024, null=True)
    event = CharField(max_length=255, null=True)
    expires = IntegerField(null=True)
    full_from = CharField(max_length=255, null=True)
    full_to = CharField(max_length=255, null=True)
    full_via = CharField(max_length=255, null=True)
    hostname = CharField(max_length=255, null=True)
    network_ip = CharField(max_length=255, null=True)
    network_port = CharField(max_length=6, null=True)
    orig_proto = CharField(max_length=255, null=True)
    presence_hosts = CharField(max_length=255, null=True)
    profile_name = CharField(max_length=255, null=True)
    proto = CharField(max_length=255, null=True)
    sip_host = CharField(max_length=255, null=True)
    sip_user = CharField(max_length=255, null=True)
    sub_to_host = CharField(max_length=255, null=True)
    sub_to_user = CharField(max_length=255, null=True)
    user_agent = CharField(max_length=255, null=True)
    version = IntegerField()

    class Meta:
        db_table = 'sip_subscriptions'

