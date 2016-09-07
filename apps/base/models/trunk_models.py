# coding=utf-8
'''
Trunks/Gateways (中继/网关)
'''

from django.db import models

    
class Trunk(models.Model):
    
    name = models.CharField(u'名称', max_length=64, blank=True, null=True)
    ttype = models.CharField(u'类型', max_length=10, choices=[('sip',u'SIP'),('iax2',u'IAX2')], default='sip')
    server = models.CharField(u'域(Realm)', max_length=64, blank=True, null=True)
    
    sip_interface = models.ForeignKey('base.SipInterface', verbose_name="绑定接口", related_name='gateways')
    context = models.ForeignKey('base.Context', verbose_name="所属组", default=1)
    
    simpleroute_caller_id_name = models.CharField(u'Caller ID Name', max_length=64, blank=True,null=True)
    simpleroute_caller_id_number = models.CharField(u'Caller ID Number', max_length=64, blank=True,null=True)
    simpleroute_area_code = models.CharField(u'本地区域代码', max_length=64, blank=True,null=True)
    
    sip_username = models.CharField(u'用户名', max_length=64, blank=True,null=True)
    sip_password = models.CharField(u'密码', max_length=64, blank=True,null=True)
    sip_from_domain = models.CharField(u'来自域', max_length=64, blank=True,null=True)
    
    sip_to_user = models.BooleanField(u'Inbound DID in To-User')
    
    sip_caller_id_field = models.CharField(u'Outbound Caller ID Field', max_length=10, choices=[('rpid',u'Remote-Party-Id'),('pid',u'P-Asserted-Identity'),('from',u'From: Field')], default='rpid')
    sip_cid_format = models.PositiveSmallIntegerField('Caller ID Format', choices=((1, '10 Digits'),(2, 'E.164 (+1)@ip.address')) , default=1)
    sip_invite_format = models.PositiveSmallIntegerField('SIP Invite Format', choices=((1, '10 Digits@ip.address'),(2, 'E.164 (+1)@ip.address'),(4, 'username@ip.address')) , default=1)
    
    # other
    from_user = ''
    proxy = ''
    register_proxy = ''
    expire_seconds = 600
    register_transport = 'udp'
    retry_seconds = 30
    caller_id_in_from = False
    contact_params = ''
    rfc5626 = True
    ping = "60"

    class Meta:
        app_label = 'base'
        verbose_name = u'中继网关'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.name
    
    def get_extension(self):
        if self.inbound:
            return self.inbound
        elif self.sip_to_user:
            return "auto_to_user"
        else:
            return None
    def get_register(self):
        if self.sip_username:
            return True
        else:
            return False
    
    
class TrunkRoutePattern(models.Model):
    
    trunk = models.ForeignKey(Trunk, verbose_name="所属中继", related_name='routepatterns')
    route = models.ForeignKey('base.Route', verbose_name="路由规则")
    prepend = models.CharField('Prepend calls with', max_length=64, blank=True,null=True)
    
    class Meta:
        app_label = 'base'
        verbose_name = u'中继路由规则'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.prepend