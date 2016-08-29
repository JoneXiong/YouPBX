# coding=utf-8

from django.db import models

'''
profiles
'''

class SipInterface(models.Model):
    
    name = models.CharField(u'名称', max_length=64, blank=True,null=True)
    ip_address = models.CharField(u'绑定IP', max_length=64)
    port = models.IntegerField(u'端口', default=5060)
    ext_ip_address = models.CharField(u'外网IP', max_length=64, blank=True,null=True)
    auth = models.BooleanField(u'需要验证', default=True)
    multiple = models.BooleanField(u'允许多机注册到同一号码')
    behind_nat = models.BooleanField(u'是否自动NAT穿透', default=True)
    nat_type = models.PositiveSmallIntegerField('匹配类型', choices=((1, 'Detect IP via uPnP'),(2, 'Detect IP via STUN Server')) , default=1)
    nat_net_list = models.ForeignKey('base.Netlist', verbose_name="网络控制", blank=True,null=True, related_name='nat_nets')
    inbound_net_list = models.ForeignKey('base.Netlist', verbose_name="呼入控制", blank=True,null=True, related_name=' inbound_nets')
    register_net_list = models.ForeignKey('base.Netlist', verbose_name="注册控制", blank=True,null=True, related_name='register_nets')
    context = models.ForeignKey('base.Context', verbose_name="所属组", default=1)
    registry_compact_headers = models.BooleanField(u'压缩头数据')
    registry_detect_nat_on_registration = models.BooleanField(u'主动NAT探测')
    registry_force_rport = models.BooleanField(u'用网络IP端口作为RTP')
    
    class Meta:
        app_label = 'base'
        verbose_name = u'SIP接口设置'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.name
    
    
    def _get_first(model_name):
        def wrapper(obj, cr, uid, context):
            model = obj.pool.get(model_name)
            ids = model.search(cr, uid, [], context=context)
            return ids[0] if ids else False
        return wrapper
