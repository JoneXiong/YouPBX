# coding=utf-8

from django.db import models

'''
Switch profile(SIP端口配置)
'''

class SipInterface(models.Model):
    '''
    Profile
    '''

    name = models.CharField(u'名称', max_length=64, blank=True,null=True)

    ip_address = models.CharField(u'绑定IP', max_length=64, blank=True,null=True, help_text='留空表示让FS自动检测')
    port = models.IntegerField(u'端口', default=5060)
    ext_ip_address = models.CharField(u'外网IP', max_length=64, blank=True,null=True)

    context = models.ForeignKey('base.Context', verbose_name="路由组(Context)", default=1)

    auth = models.BooleanField(u'需要验证', default=True)
    multiple = models.BooleanField(u'允许多机注册到同一号码')
    behind_nat = models.BooleanField(u'是否自动NAT穿透', default=True)

    nat_type = models.PositiveSmallIntegerField('NAT穿透方式', choices=((1, 'Detect IP via uPnP'),(2, 'Detect IP via STUN Server')) , default=1)

    nat_net_list = models.ForeignKey('base.Netlist', verbose_name="网络控制", blank=True,null=True, related_name='nat_nets')
    inbound_net_list = models.ForeignKey('base.Netlist', verbose_name="呼入控制", blank=True,null=True, related_name='inbound_nets')
    register_net_list = models.ForeignKey('base.Netlist', verbose_name="注册控制", blank=True,null=True, related_name='register_nets')

    # 注册登记相关
    registry_compact_headers = models.BooleanField(u'Registry压缩头数据')
    registry_detect_nat_on_registration = models.BooleanField(u'Registry主动NAT探测')
    registry_force_rport = models.BooleanField(u'Registry用网络IP端口作为RTP(rport)')

    #other
    manage_presence = True
    presence_db_name = 'share_presence'
    presence_hosts = 'sip.mydomain.com'
    send_presence_on_register = True
    delete_subs_on_register = True
    caller_id_type = u'rpid'
    auto_jitterbuffer_msec = 120

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

    minimum_session_expires = 120
    vm_from_email = u'voicemail@freeswitch.org'
    disable_register = False
    log_auth_failures = True
    auth_all_packets = False

    class Meta:
        app_label = 'base'
        verbose_name = u'端口(Profile)'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '%s %s'%(self.name ,self.port)


    def _get_first(model_name):
        def wrapper(obj, cr, uid, context):
            model = obj.pool.get(model_name)
            ids = model.search(cr, uid, [], context=context)
            return ids[0] if ids else False
        return wrapper

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
