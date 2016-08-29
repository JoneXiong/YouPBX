# coding=utf-8

from django.db import models

    
class RingGroup(models.Model):
    
    name = models.CharField(u'名称', max_length=64)
    location = models.ForeignKey('base.Location', verbose_name="所属域", default=1)
    strategy = models.PositiveSmallIntegerField('策略', choices=((4, 'Ring All'),(2, 'Ring In Order')) , default=4)
    number = models.ForeignKey('base.Number', verbose_name="选择号码")
    
    class Meta:
        app_label = 'funcs'
        verbose_name = u'来电队列'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.name
    
    
class RingGroupDevice(models.Model):
    
    ring_group = models.ForeignKey(RingGroup, verbose_name="所属队列")
    orderby_int = models.IntegerField(u'排序' , blank=True, null=True)
    device = models.ForeignKey('funcs.Device', verbose_name="选择成员")
    
    class Meta:
        app_label = 'funcs'
        verbose_name = u'来电队列成员分机'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.device
