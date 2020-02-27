# coding=utf-8
'''
时间安排
'''

from django.db import models

class WeekCondition(models.Model):

    name = models.CharField('名称', max_length=64)
    priority = models.IntegerField('优先级',default=1)
    day_start = models.CharField('从(例08:00)',max_length=64)
    day_end = models.CharField('到(例18:00)',max_length=64)
    day_list = models.CharField('星期', max_length=64)

    class Meta:
        app_label = 'funcs'
        verbose_name = u'星期时间条件'
        verbose_name_plural = verbose_name

class PeriodCondition(models.Model):

    name = models.CharField('名称', max_length=64)
    priority = models.IntegerField('优先级',default=1)
    period_start = models.DateTimeField('开始时间')
    period_end = models.DateTimeField('结束时间')

    class Meta:
        app_label = 'funcs'
        verbose_name = u'固定时间条件'
        verbose_name_plural = verbose_name

