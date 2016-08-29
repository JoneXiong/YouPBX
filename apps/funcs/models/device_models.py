# coding=utf-8

from django.db import models


class Device(models.Model):
    
    name = models.CharField(u'名称', max_length=64)
    class_type = models.CharField(u'类型', max_length=20, choices=[('SipDevice',u'SIP device')], default='SipDevice')
    context = models.ForeignKey('base.Context', verbose_name="默认组", default=1)
    location = models.ForeignKey('base.Location', verbose_name="所属域", default=1)
    
    callerid_internal_name = models.CharField(u'内部名称', max_length=64, blank=True, null=True)
    callerid_internal_number = models.CharField(u'内部号码', max_length=64, blank=True, null=True)
    callerid_external_name = models.CharField(u'外部名称', max_length=64, blank=True, null=True)
    callerid_external_number = models.CharField(u'外部号码', max_length=64, blank=True, null=True)
    media_mode = models.CharField(u'音频传输模式', max_length=10, choices=[('psp',u'服务器中转'),('p2p',u'点对点')], default='psp')
    
    sip_username = models.CharField(u'SIP用户名', max_length=64, blank=True, null=True)
    sip_password = models.CharField(u'SIP密码', max_length=64, blank=True, null=True)
    
    sip_caller_id_field = models.CharField(u'Outbound Caller ID Field', max_length=10, choices=[('rpid',u'Remote-Party-Id'),('pid',u'P-Asserted-Identity'),('from',u'From: Field')], default='rpid')
    sip_cid_format = models.PositiveSmallIntegerField('Caller ID Format', max_length=20, choices=((1, '10 Digits'),(2, 'E.164 (+1)')) , default=1)
    sip_invite_format = models.PositiveSmallIntegerField('SIP Invite Format', max_length=50, choices=((1, '10 Digits@ip.address'),(2, 'E.164 (+1)@ip.address'),(4, 'username@ip.address')) , default=1)
    
    voicemail = models.ForeignKey('funcs.VoiceMail', verbose_name="发送通知邮箱", blank=True, null=True)
    number = models.ForeignKey('base.Number', verbose_name="选择号码")
    registry_ringtype = models.CharField(u'响铃模式', max_length=10, choices=[('ringing',u'Ringing'), ('moh',u'Hold Music')], default='ringing')
    registry_timeout = models.IntegerField(u'响铃时长(秒)', default=30)
    registry_ignoreFWD = models.BooleanField(u'禁用呼叫转发')
    
    class Meta:
        app_label = 'funcs'
        verbose_name = u'分机'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.name
    
