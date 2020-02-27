# coding=utf-8
'''
Extension(电话分机)
'''

from django.db import models


class Device(models.Model):

    name = models.CharField(u'号码', max_length=64)
    class_type = models.CharField(u'类型', max_length=20, choices=[
                                                                 ('SipDevice',u'SIP device'),
                                                                 ('IAX2Device',u'IAX2 device'),
                                                                 ('FXSDevice',u'FXS device'),
                                                                 ], default='SipDevice')
    context = models.ForeignKey('base.Context', verbose_name="默认组", default=1)
    location = models.ForeignKey('base.Location', verbose_name="所属域", default=1, related_name="devices")

    callerid_internal_name = models.CharField(u'内部名称', max_length=64, blank=True, null=True)
    callerid_internal_number = models.CharField(u'内部号码', max_length=64, blank=True, null=True)

    callerid_external_name = models.CharField(u'外部名称', max_length=64, blank=True, null=True)
    callerid_external_number = models.CharField(u'外部号码', max_length=64, blank=True, null=True)

    media_mode = models.CharField(u'音频传输模式', max_length=10, choices=[('psp',u'服务器中转'),('p2p',u'点对点')], default='psp')

    sip_username = models.CharField(u'SIP名字', max_length=64, blank=True, null=True)
    sip_password = models.CharField(u'SIP密码', max_length=64, blank=True, null=True)

    sip_caller_id_field = models.CharField(u'Outbound Caller ID Field', max_length=10, choices=[('rpid',u'Remote-Party-Id'),('pid',u'P-Asserted-Identity'),('from',u'From: Field')], default='rpid')
    sip_cid_format = models.PositiveSmallIntegerField('Caller ID Format', max_length=20, choices=((1, '10 Digits'),(2, 'E.164 (+1)')) , default=1)
    sip_invite_format = models.PositiveSmallIntegerField('SIP Invite Format', max_length=50, choices=((1, '10 Digits@ip.address'),(2, 'E.164 (+1)@ip.address'),(4, 'username@ip.address')) , default=1)

    voicemail = models.ForeignKey('funcs.VoiceMail', verbose_name="发送通知邮箱", blank=True, null=True)
    number = models.ForeignKey('base.Number', blank=True, null=True,editable=False)
    mobile = models.CharField(u'手机号', max_length=64, blank=True, null=True)
    db_name = models.CharField(u'所在db', max_length=64, blank=True, null=True)
    ukey = models.CharField(u'用户标识', max_length=64, blank=True, null=True)

    registry_ringtype = models.CharField(u'响铃模式', max_length=10, choices=[('ringing',u'Ringing'), ('moh',u'Hold Music')], default='ringing')
    registry_timeout = models.IntegerField(u'响铃时长(秒)', default=30)
    registry_ignoreFWD = models.BooleanField(u'禁用呼叫转发', default=False)

    # other
    sip_force_contact = 'nat-connectile-dysfunction'
    transfer_fallback_extension = 'operator'

    class Meta:
        app_label = 'funcs'
        verbose_name = u'分机'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '%s %s'%(self.name, self.sip_username or '')


    def get_trunk_key(self):
        context = self.context
        trunks = context.context_trunks.all()
        if trunks:
            return trunks[0].get_trunk_key()
        else:
            return 'trunk_0'

    def get_callstr(self, answer_type, answer_number=None):
        if answer_type=='mobile':
            answer_number = answer_number or self.mobile
            return 'sofia/gateway/%s/|%s'%(self.get_trunk_key(), answer_number)
        else:
            answer_number = answer_number or self.name
            return 'user/|%s@%s'%(answer_number, self.location.domain_name)


    def get_callee_str(self, callee):
        if len(str(callee))>4:
            return 'sofia/gateway/%s/|%s'%(self.get_trunk_key(), callee)
        else:
            return 'user/|%s@120.77.171.50'%callee
