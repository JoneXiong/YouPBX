# -*- coding: utf-8 -*-

from peewee import *

import config 

database = SqliteDatabase(config.fs_db_path+'call_limit.db', check_same_thread=False, **{})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class DbData(BaseModel):
    data = CharField(max_length=255, null=True)
    data_key = CharField(max_length=255, null=True)
    hostname = CharField(max_length=255, null=True)
    realm = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'db_data'

class GroupData(BaseModel):
    groupname = CharField(max_length=255, null=True)
    hostname = CharField(max_length=255, null=True)
    url = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'group_data'

class LimitData(BaseModel):
    hostname = CharField(max_length=255, null=True)
    id = CharField(max_length=255, null=True)
    realm = CharField(max_length=255, null=True)
    uuid = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'limit_data'

