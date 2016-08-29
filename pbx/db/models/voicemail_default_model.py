# -*- coding: utf-8 -*-

from peewee import *
from mocrud.admin import ModelAdmin
import config

database = SqliteDatabase(config.fs_db_path+'voicemail_default.db', check_same_thread=False, **{})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class VoicemailMsgs(BaseModel):
    uuid = CharField(max_length=255, null=True, verbose_name=u'UUID')
    cid_name = CharField(max_length=255, null=True, verbose_name=u'留言人名称')
    cid_number = CharField(max_length=255, null=True, verbose_name=u'留言人号码')
    username = CharField(max_length=255, null=True, verbose_name=u'接收人')
    created_epoch = IntegerField(null=True, verbose_name=u'留言时间')
    domain = CharField(max_length=255, null=True)
    file_path = CharField(max_length=255, null=True, verbose_name=u'录音文件')
    flags = CharField(max_length=255, null=True, verbose_name=u'状态')
    forwarded_by = CharField(max_length=255, null=True)
    in_folder = CharField(max_length=255, null=True)
    message_len = IntegerField(null=True, verbose_name=u'长度')
    read_epoch = IntegerField(null=True, verbose_name=u'收听时间')
    read_flags = CharField(max_length=255, null=True, verbose_name=u'收听状态')#B_NORMAL

    class Meta:
        db_table = 'voicemail_msgs'
        
class VoicemailMsgsAdmin(ModelAdmin):
    verbose_name = u'语音留言'
    method_exclude = ['add', 'delete', 'edit']
VoicemailMsgs.Admin = VoicemailMsgsAdmin

class VoicemailPrefs(BaseModel):
    domain = CharField(max_length=255, null=True)
    greeting_path = CharField(max_length=255, null=True)
    name_path = CharField(max_length=255, null=True)
    password = CharField(max_length=255, null=True)
    username = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'voicemail_prefs'

