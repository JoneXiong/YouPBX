# -*- coding: utf-8 -*-
from peewee import *

database = PostgresqlDatabase('pbx', **{'user': 'openerp','password': 'openerp'})

class UnknownFieldType(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database
        
class Fs_Media_File(BaseModel):
    comment = TextField(null=True)
#    create_date = DateTimeField(null=True)
#    create_uid = ForeignKeyField(null=True, db_column='create_uid', rel_model=Res_Users)
    db_datas = BlobField(null=True)
    file_size = IntegerField(null=True)
    is_folder = BooleanField(null=True)
    name = CharField(null=True)
    parent = ForeignKeyField(null=True, db_column='parent_id', rel_model='self')
    path = CharField(null=True)
#    write_date = DateTimeField(null=True)
#    write_uid = ForeignKeyField(null=True, db_column='write_uid', rel_model=Res_Users)

    class Meta:
        db_table = 'fs_media_file'
 
class Fs_Location(BaseModel):
    domain_name = CharField()
    location_name = CharField()

    class Meta:
        db_table = 'fs_location'       
        
class Fs_Context(BaseModel):
    name = CharField()
    media_mode = CharField()
    endtype = CharField()
    tts_string = CharField()
    media_file = ForeignKeyField(db_column='media_file_id', rel_model=Fs_Media_File)

    class Meta:
        db_table = 'fs_context'
        
class Fs_Netlist(BaseModel):
    
    default_type = CharField()
    name = CharField(null=True)
    systemlist = CharField(null=True)
    
    def get_name(self):
        if self.systemlist:
            return self.systemlist
        else:
            return "net_list_%s"%self.id

    class Meta:
        db_table = 'fs_netlist'

class Fs_Netlist_Item(BaseModel):

    netlist = ForeignKeyField(db_column='netlist_id', rel_model=Fs_Netlist, related_name='items')
    record = CharField()
    type = CharField()

    class Meta:
        db_table = 'fs_netlist_item'
        
class Fs_Sipinterface(BaseModel):
    name = CharField(null=True)

    manage_presence = True
    presence_db_name = 'share_presence'
    presence_hosts = 'sip.mydomain.com'
    send_presence_on_register = True
    delete_subs_on_register = True
    caller_id_type = u'rpid'
    auto_jitterbuffer_msec = 120
    nat_type = CharField()
    ext_ip_address = CharField(null=True)
    ip_address = CharField(null=True)
    sip_port = IntegerField(db_column='port')
    nonce_ttl = '86400'
    use_rtp_timer = True
    rtp_timer_name = 'soft'
    codec_prefs = '$${global_codec_prefs}'
    inbound_codec_negotiation = 'generous'
    rtp_timeout_sec = 300
    rtp_hold_timeout_sec = 1800
    rfc2833_pt = 101
    dtmf_duration = 100
    dtmf_type = u'rfc2833'
    session_timeout = 1800
    codec_ms = 20
    accept_blind_reg = False
    auth_calls = BooleanField(db_column='auth',null=True)
    multiple_registrations = BooleanField(db_column='multiple',null=True)
    #multiple_registrations = u'contact' #true
    minimum_session_expires = 120
    vm_from_email = u'voicemail@freeswitch.org'
    disable_register = False
    log_auth_failures = True
    auth_all_packets = False
    
    behind_nat = BooleanField(null=True, default=True)
    context = ForeignKeyField(db_column='context_id', rel_model=Fs_Context)
    
    nat_net_list = ForeignKeyField(null=True, db_column='nat_net_list_id', rel_model=Fs_Netlist,related_name='a')
    inbound_net_list = ForeignKeyField(null=True, db_column='inbound_net_list_id', rel_model=Fs_Netlist,related_name='b')
    register_net_list = ForeignKeyField(null=True, db_column='register_net_list_id', rel_model=Fs_Netlist,related_name='c')
    
    registry_compact_headers = BooleanField(null=True)
    registry_detect_nat_on_registration = BooleanField(null=True)
    registry_force_rport = BooleanField(null=True)
    
    def get_ext_ip(self):
        if self.ext_ip_address:
            if self.nat_type:
                return "autonat:" + self.ext_ip_address
            else:
                return self.ext_ip_address
        elif str(self.nat_type) == str(1):
            return 'auto-nat'
        elif str(self.nat_type) == str(2):
            return 'stun:stun.freeswitch.org'
            

    class Meta:
        db_table = 'fs_sipinterface'
        
class Fs_Route(BaseModel):

    description = CharField(null=True)
    name = CharField()
    type = CharField()

    class Meta:
        db_table = 'fs_route'
        
    def get_expression(self):
        convert = self.type=='2'
        pattern_list = [ convert and '^%s$'%obj.content or obj.content  for obj in self.patterns ]
        return '|'.join(pattern_list)

class Fs_Route_Pattern(BaseModel):
    content = CharField()
    route = ForeignKeyField(db_column='route_id', rel_model=Fs_Route, related_name='patterns')

    class Meta:
        db_table = 'fs_route_pattern'
        
class Fs_Trunk(BaseModel):
    name = CharField(null=True)
    username = CharField(db_column='sip_username', null=True)
    password = CharField(db_column='sip_password', null=True)
    realm = CharField(db_column='server', null=True)
    from_user = ''
    from_domain = CharField(db_column='sip_from_domain', null=True)
    proxy = ''
    register_proxy = ''
    expire_seconds = 600
    register_transport = 'udp'
    retry_seconds = 30
    caller_id_in_from = False
    contact_params = ''
    rfc5626 = True
    ping = "60"
    
    context = ForeignKeyField(null=True, db_column='context_id', rel_model=Fs_Context)
    
    simpleroute_area_code = CharField(null=True)
    simpleroute_caller_id_name = CharField(null=True)
    simpleroute_caller_id_number = CharField(null=True)
    sip_caller_id_field = CharField(null=True)
    sip_cid_format = CharField(null=True)

    sip_invite_format = CharField(null=True)

    sip_to_user = BooleanField(null=True)

    sipinterface = ForeignKeyField(null=True, db_column='sipinterface_id', rel_model=Fs_Sipinterface, related_name='gateways')
    type = CharField()
    
    def get_extension(self):
        if self.inbound:
            return self.inbound
        elif self.to_user:
            return "auto_to_user"
        else:
            return None
    def get_register(self):
        if self.username:
            return True
        else:
            return False

    class Meta:
        db_table = 'fs_trunk'

class Fs_Trunk_Routepattern(BaseModel):
    prepend = CharField()
    route = ForeignKeyField(db_column='route_id', rel_model=Fs_Route)
    trunk = ForeignKeyField(db_column='trunk_id', rel_model=Fs_Trunk)

    class Meta:
        db_table = 'fs_trunk_routepattern'
        
class Fs_Numberpool(BaseModel):
    alias = CharField(null=True)
    count = IntegerField(null=True)
    name = CharField()
    no = CharField(null=True)

    class Meta:
        db_table = 'fs_numberpool'

class Fs_Number(BaseModel):
    context = ForeignKeyField(null=True, db_column='context_id', rel_model=Fs_Context)
    location = ForeignKeyField(null=True, db_column='location_id', rel_model=Fs_Location)
    number = CharField()
    numberpool = ForeignKeyField(null=True, db_column='numberpool_id', rel_model=Fs_Numberpool)
    terminate_action = CharField()
    #transfer_voicemail = IntegerField(null=True, db_column='transfer_voicemail_id')
    voicemail = IntegerField(null=True, db_column='voicemail_id')
    
    def get_vm_number(self):
        pass
    
    def get_transfer_number(self):
        pass

    class Meta:
        db_table = 'fs_number'
        
        
class Fs_Voicemail(BaseModel):
    mailbox = CharField(null=True)
    name = CharField()
    vm_password = CharField(db_column='password', null=True)
    
    vm_email = CharField(db_column='registry_email_address', null=True)
    vm_attach_email  = BooleanField(db_column='registry_email_all_messages', null=True)
    vm_attach_file = BooleanField(db_column='registry_attach_audio_file', null=True)
    vm_delete_file = BooleanField(db_column='registry_delete_file',null=True)

    vm_notify_email = False
    timezone = 'Asia/Hong_Kong'
    
    number = ForeignKeyField(db_column='number_id', rel_model=Fs_Number)
    skipgreeting = BooleanField(null=True, db_column='skipGreeting')
    skipinstructions = BooleanField(null=True, db_column='skipInstructions')

    class Meta:
        db_table = 'fs_voicemail'
        
#class Fs_Voicemail_Number(BaseModel):
#    number = ForeignKeyField(db_column='number_id', rel_model=Fs_Number)
#    skipgreeting = BooleanField(null=True, db_column='skipGreeting')
#    skipinstructions = BooleanField(null=True, db_column='skipInstructions')
#    voicemail = ForeignKeyField(db_column='voicemail_id', rel_model=Fs_Voicemail)
#
#    class Meta:
#        db_table = 'fs_voicemail_number'
        
class Fs_Device(BaseModel):
    outbound_caller_id_name = CharField(db_column='callerid_external_name', null=True)
    outbound_caller_id_number = CharField(db_column='callerid_external_number', null=True)
    internal_caller_id_name = CharField(db_column='callerid_internal_name', null=True) 
    internal_caller_id_number = CharField(db_column='callerid_internal_number', null=True)
    
    sip_force_contact = 'nat-connectile-dysfunction'
    transfer_fallback_extension = 'operator'
    
    class_type = CharField()
    context = ForeignKeyField(null=True, db_column='context_id', rel_model=Fs_Context)
    location = ForeignKeyField(null=True, db_column='location_id', rel_model=Fs_Location, related_name='devices')
    media_mode = CharField()
    name = CharField()
    sip_caller_id_field = CharField(null=True)
    sip_cid_format = CharField(null=True)
    sip_invite_format = CharField(null=True)
    sip_password = CharField(null=True)
    sip_username = CharField(null=True)
    voicemail = ForeignKeyField(null=True, db_column='voicemail_id', rel_model=Fs_Voicemail)
    
    number = ForeignKeyField(db_column='number_id', rel_model=Fs_Number)
    registry_ignorefwd = BooleanField(null=True, db_column='registry_ignoreFWD')
    registry_ringtype = CharField()
    registry_timeout = IntegerField(null=True)

    class Meta:
        db_table = 'fs_device'
        
#class Fs_Device_Number(BaseModel):
#    device = ForeignKeyField(db_column='device_id', rel_model=Fs_Device)
#    number = ForeignKeyField(db_column='number_id', rel_model=Fs_Number)
#    registry_ignorefwd = BooleanField(null=True, db_column='registry_ignoreFWD')
#    registry_ringtype = CharField()
#    registry_timeout = IntegerField(null=True)
#
#    class Meta:
#        db_table = 'fs_device_number'
        
class Fs_Ringgroup(BaseModel):
    location = ForeignKeyField(db_column='location_id', rel_model=Fs_Location)
    name = CharField()
    strategy = CharField()
    number = ForeignKeyField(db_column='number_id', rel_model=Fs_Number)

    class Meta:
        db_table = 'fs_ringgroup'

class Fs_Ringgroup_Device(BaseModel):
    device = ForeignKeyField(db_column='device_id', rel_model=Fs_Device)
    orderbyint = IntegerField(null=True)
    ringgroup = ForeignKeyField(db_column='ringgroup_id', rel_model=Fs_Ringgroup,related_name='members')

    class Meta:
        db_table = 'fs_ringgroup_device'

#class Fs_Ringgroup_Number(BaseModel):
#    number = ForeignKeyField(db_column='number_id', rel_model=Fs_Number)
#    ringgroup = ForeignKeyField(db_column='ringgroup_id', rel_model=Fs_Ringgroup)
#
#    class Meta:
#        db_table = 'fs_ringgroup_number'

class Fs_Autoattendant(BaseModel):
    digit_timeout = IntegerField(null=True)
    extension_context = ForeignKeyField(null=True, db_column='extension_context_id', rel_model=Fs_Context)
    extension_digits = IntegerField(null=True)
    name = CharField()
    registry_max_failures = IntegerField(null=True)
    registry_mediafile = ForeignKeyField(db_column='registry_mediafile_id', rel_model=Fs_Media_File)
    registry_tts_string = TextField(null=True)
    registry_type = CharField()
    timeout = IntegerField(null=True)
    number = ForeignKeyField(db_column='number_id', rel_model=Fs_Number)

    class Meta:
        db_table = 'fs_autoattendant'

class Fs_Autoattendant_Keymapping(BaseModel):
    autoattendant = ForeignKeyField(db_column='autoattendant_id', rel_model=Fs_Autoattendant)
    class_type = CharField()
    digits = CharField()
    voicemail = ForeignKeyField(null=True, db_column='voicemail_id', rel_model=Fs_Voicemail)

    class Meta:
        db_table = 'fs_autoattendant_keymapping'

#class Fs_Autoattendant_Number(BaseModel):
#    autoattendant = ForeignKeyField(db_column='autoattendant_id', rel_model=Fs_Autoattendant)
#    number = ForeignKeyField(db_column='number_id', rel_model=Fs_Number)
#
#    class Meta:
#        db_table = 'fs_autoattendant_number'

class Fs_Conference(BaseModel):
    name = CharField()
    pin = CharField()
    registry_energy_level = IntegerField(null=True)
    registry_comfort_noise = BooleanField(null=True)
    registry_moh_type = CharField()
    registry_record = BooleanField(null=True)
    number = ForeignKeyField(db_column='number_id', rel_model=Fs_Number)

    class Meta:
        db_table = 'fs_conference'

#class Fs_Conference_Number(BaseModel):
#    conference = ForeignKeyField(db_column='conference_id', rel_model=Fs_Device)
#    number = ForeignKeyField(db_column='number_id', rel_model=Fs_Number)
#
#    class Meta:
#        db_table = 'fs_conference_number'

class Fs_Config_Settings(BaseModel):
    flag = BooleanField(null=True)

    class Meta:
        db_table = 'fs_config_settings'

class Fs_TimeRoutes(BaseModel):
    name = CharField()
    time_from = DateTimeField()
    time_to = DateTimeField()
    number = ForeignKeyField(db_column='number_id', rel_model=Fs_Number)
    
    class Meta:
        db_table = 'fs_timeroutes'
        
    def get_during_transger_number(self):
        pass
    
    def get_outside_transger_number(self):
        pass

