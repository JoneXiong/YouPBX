# -*- coding: utf-8 -*-

import time

from peewee import *
from mocrud.admin import ModelAdmin
import config

database = SqliteDatabase(config.fs_db_path+'core.db', check_same_thread=False, **{})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class Aliases(BaseModel):
    alias = CharField(max_length=128, null=True, verbose_name=u'别名')
    command = CharField(max_length=4096, null=True, verbose_name=u'命令内容')
    hostname = CharField(max_length=256, null=True, verbose_name=u'主机名')
    sticky = IntegerField(null=True, verbose_name=u'重启是否保留')

    class Meta:
        db_table = 'aliases'

class Calls(BaseModel):
    u'''
    通话
    '''
    call_created = CharField(max_length=128, null=True, verbose_name=u'创建时间')
    call_created_epoch = IntegerField(null=True, verbose_name=u'时间戳')
    call_uuid = CharField(max_length=255, null=True, verbose_name=u'呼叫ID (主叫通道ID)')
    caller_uuid = CharField(max_length=256, null=True, verbose_name=u'主叫通道ID')
    callee_uuid = CharField(max_length=256, null=True, verbose_name=u'被叫通道ID')
    hostname = CharField(max_length=256, null=True)

    class Meta:
        db_table = 'calls'

class Channels(BaseModel):
    u'''
    通道
    '''
    application = CharField(max_length=128, null=True, verbose_name=u'动作应用')
    application_data = CharField(max_length=4096, null=True, verbose_name=u'应用数据')
    
    call_uuid = CharField(max_length=256, null=True, verbose_name=u'呼叫ID (主叫通道ID)')
    callstate = CharField(max_length=64, null=True, verbose_name=u'呼叫状态')
    
    callee_direction = CharField(max_length=5, null=True, verbose_name=u'被叫方向')
    callee_name = CharField(max_length=1024, null=True, verbose_name=u'被叫名称')
    callee_num = CharField(max_length=256, null=True, verbose_name=u'被叫号码')

    cid_name = CharField(max_length=1024, null=True, verbose_name=u'主叫名称')
    cid_num = CharField(max_length=256, null=True, verbose_name=u'主叫号码')
    
    context = CharField(max_length=128, null=True, verbose_name=u'所属context')
    created = CharField(max_length=128, null=True, verbose_name=u'创建时间')
    created_epoch = IntegerField(null=True, verbose_name=u'时间戳')
    dest = CharField(max_length=1024, null=True, verbose_name=u'目的地')
    dialplan = CharField(max_length=128, null=True)
    direction = CharField(max_length=32, null=True)
    
    hostname = CharField(max_length=256, null=True)
    ip_addr = CharField(max_length=256, null=True)
    
    name = CharField(max_length=1024, null=True)
    presence_data = CharField(max_length=4096, null=True)
    presence = CharField(db_column='presence_id', max_length=4096, null=True)
    read_bit_rate = CharField(max_length=32, null=True)
    read_codec = CharField(max_length=128, null=True)
    read_rate = CharField(max_length=32, null=True)
    secure = CharField(max_length=32, null=True)
    sent_callee_name = CharField(max_length=1024, null=True)
    sent_callee_num = CharField(max_length=256, null=True)
    state = CharField(max_length=64, null=True)
    uuid = CharField(max_length=256, null=True, verbose_name=u'通道ID')
    write_bit_rate = CharField(max_length=32, null=True)
    write_codec = CharField(max_length=128, null=True)
    write_rate = CharField(max_length=32, null=True)

    class Meta:
        db_table = 'channels'
        
class ChannelsAdmin(ModelAdmin):
    verbose_name = u'当前呼叫'
    columns = ('uuid', 'cid_num', 'callee_num', 'callstate', 'context', 'created', 'application')
    method_exclude = ['add', 'delete', 'edit']
    
#    def get_template_overrides(self):
#        '''
#        定义crud的基础模板
#        '''
#        return {
#                'index': 'channels_index.html',
#                }
    # 列表 direction = inbound
    # 状态判断 callstate = EARLY 呼叫中 ACTIVE 通话中
Channels.Admin = ChannelsAdmin

class Complete(BaseModel):
    u'''
    命令自动补全
    '''
    a1 = CharField(max_length=128, null=True)
    a10 = CharField(max_length=128, null=True)
    a2 = CharField(max_length=128, null=True)
    a3 = CharField(max_length=128, null=True)
    a4 = CharField(max_length=128, null=True)
    a5 = CharField(max_length=128, null=True)
    a6 = CharField(max_length=128, null=True)
    a7 = CharField(max_length=128, null=True)
    a8 = CharField(max_length=128, null=True)
    a9 = CharField(max_length=128, null=True)
    hostname = CharField(max_length=256, null=True)
    sticky = IntegerField(null=True)

    class Meta:
        db_table = 'complete'

class Interfaces(BaseModel):
    u'''
    接口
    '''
    description = CharField(max_length=4096, null=True, verbose_name=u'描述')
    filename = CharField(max_length=4096, null=True, verbose_name=u'某块文件路径')
    hostname = CharField(max_length=256, null=True)
    ikey = CharField(max_length=1024, null=True)
    name = CharField(max_length=1024, null=True)
    syntax = CharField(max_length=4096, null=True)
    type = CharField(max_length=128, null=True)

    class Meta:
        db_table = 'interfaces'

class Nat(BaseModel):
    hostname = CharField(max_length=256, null=True)
    port = IntegerField(null=True)
    proto = IntegerField(null=True)
    sticky = IntegerField(null=True)

    class Meta:
        db_table = 'nat'

class Recovery(BaseModel):
    hostname = CharField(max_length=255, null=True)
    metadata = TextField(null=True)
    profile_name = CharField(max_length=255, null=True)
    runtime_uuid = CharField(max_length=255, null=True)
    technology = CharField(max_length=255, null=True)
    uuid = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'recovery'

class Registrations(BaseModel):
    u'''
    当前注册的用户(基础)
    '''
    expires = IntegerField(null=True, verbose_name=u'过期时间')
    hostname = CharField(max_length=256, null=True, verbose_name=u'服务器名')
    metadata = CharField(max_length=256, null=True)
    network_ip = CharField(max_length=256, null=True, verbose_name=u'客户端IP')
    network_port = CharField(max_length=256, null=True, verbose_name=u'客户端端口')
    network_proto = CharField(max_length=256, null=True, verbose_name=u'连接协议')
    realm = CharField(max_length=256, null=True, verbose_name=u'域')
    reg_user = CharField(max_length=256, null=True, verbose_name=u'用户')
    token = CharField(max_length=256, null=True)
    url = TextField(null=True, verbose_name=u'注册URL')

    class Meta:
        db_table = 'registrations'
        
    def get_expires(self):
        ltime=time.localtime(self.expires)
        timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
        return timeStr
        
class RegistrationsAdmin(ModelAdmin):
    verbose_name = u'当前连接分机'
    method_exclude = ['add', 'delete', 'edit']
    columns = ('hostname', 'network_ip', 'network_port','network_proto', 'realm', 'reg_user', 'get_expires', 'url')
    add_column_display = {
                          'get_expires': u'过期时间',
    }
Registrations.Admin = RegistrationsAdmin

class Tasks(BaseModel):
    hostname = CharField(max_length=256, null=True)
    task_desc = CharField(max_length=4096, null=True)
    task_group = CharField(max_length=1024, null=True)
    task = IntegerField(db_column='task_id', null=True)
    task_sql_manager = IntegerField(null=True)

    class Meta:
        db_table = 'tasks'

