# -*- coding: utf-8 -*-

from peewee import *
from mocrud.admin import ModelAdmin
import config

database = SqliteDatabase(config.fs_db_path+'fifo.db', check_same_thread=False, **{})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class FifoBridge(BaseModel):
    bridge_start = IntegerField(null=True)
    caller_caller_id_name = CharField(max_length=255, null=True)
    caller_caller_id_number = CharField(max_length=255, null=True)
    caller_uuid = CharField(max_length=255)
    consumer_outgoing_uuid = CharField(max_length=255, null=True)
    consumer_uuid = CharField(max_length=255)
    fifo_name = CharField(max_length=1024)

    class Meta:
        db_table = 'fifo_bridge'
        
class FifoBridgeAdmin(ModelAdmin):
    verbose_name = u'已接听队列来电'
    method_exclude = ['add', 'delete', 'edit']
FifoBridge.Admin = FifoBridgeAdmin

class FifoCallers(BaseModel):
    caller_caller_id_name = CharField(max_length=255, null=True)
    caller_caller_id_number = CharField(max_length=255, null=True)
    fifo_name = CharField(max_length=255)
    timestamp = IntegerField(null=True)
    uuid = CharField(max_length=255)

    class Meta:
        db_table = 'fifo_callers'
        
class FifoCallersAdmin(ModelAdmin):
    verbose_name = u'待接听队列来电'
    method_exclude = ['add', 'delete', 'edit']
FifoCallers.Admin = FifoCallersAdmin

class FifoOutbound(BaseModel):
    active_time = IntegerField()
    expires = IntegerField()
    fifo_name = CharField(max_length=255, null=True)
    hostname = CharField(max_length=255, null=True)
    inactive_time = IntegerField()
    lag = IntegerField(null=True)
    manual_calls_in_count = IntegerField()
    manual_calls_in_total_count = IntegerField()
    manual_calls_out_count = IntegerField()
    manual_calls_out_total_count = IntegerField()
    next_avail = IntegerField()
    originate_string = CharField(max_length=255, null=True)
    outbound_call_count = IntegerField()
    outbound_call_total_count = IntegerField()
    outbound_fail_count = IntegerField()
    outbound_fail_total_count = IntegerField()
    ring_count = IntegerField()
    simo_count = IntegerField(null=True)
    start_time = IntegerField()
    static = IntegerField()
    status = CharField(max_length=255, null=True)
    stop_time = IntegerField()
    taking_calls = IntegerField()
    timeout = IntegerField(null=True)
    use_count = IntegerField(null=True)
    uuid = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'fifo_outbound'

