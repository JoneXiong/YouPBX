# coding=utf-8
'''
AclBlacklist  netlist (访问控制列表)
'''

from django.db import models

class Netlist(models.Model):
    
    name = models.CharField(u'名称', max_length=64, blank=True,null=True)
    systemlist = models.CharField(u'系统控制列标识', max_length=64, blank=True,null=True)
    default_type = models.CharField(u'默认类型', max_length=10, choices=[('allow',u'允许'),('deny',u'拒绝')], default='deny')
    
    class Meta:
        app_label = 'base'
        verbose_name = u'呼叫网络控制'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.name
    
    def get_name(self):
        if self.systemlist:
            return self.systemlist
        else:
            return "net_list_%s"%self.id

class NetlistItem(models.Model):
    
    netlist = models.ForeignKey(Netlist, verbose_name=u'所属控制列', related_name='items')
    models.CharField(u'默认类型', max_length=10, choices=[('allow',u'允许'),('deny',u'拒绝')], default='deny')
    record =  models.CharField(u'名称', max_length=64)
    
    class Meta:
        app_label = 'base'
        verbose_name = u'控制详细'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.record
