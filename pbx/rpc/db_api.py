# coding=utf-8

from peewee import *

import config

database = SqliteDatabase(config.fs_db_path+'sofia_reg_sipinterface_1.db', check_same_thread=False, **{})

class BaseModel(Model):
    class Meta:
        database = database


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


def get_reg_count():
    return SipRegistrations.select().count()


def is_in_reg(number):
    return SipRegistrations.select().where(SipRegistrations.sip_user==str(number)).exists()
