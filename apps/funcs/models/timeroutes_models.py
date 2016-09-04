# coding=utf-8
'''
时间安排
'''

from django.db import models


class TimeRoutes(models.Model):
    
    name = models.CharField(u'名称', max_length=64)
    during_type = models.CharField(u'时间期间转接', max_length=64, blank=True, null=True)
    outside_type = models.CharField(u'时间之外转接', max_length=64, blank=True, null=True)
    time_from = models.DateTimeField(u'从')
    time_to = models.DateTimeField(u'到')
    number = models.ForeignKey('base.Number', verbose_name=u"选择号码")
    
    class Meta:
        app_label = 'funcs'
        verbose_name = u'工作时段'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.name

    def get_during_transger_number(self):
        pass
    
    def get_outside_transger_number(self):
        pass