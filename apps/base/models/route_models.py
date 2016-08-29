# coding=utf-8

from django.db import models

class Route(models.Model):
    
    name = models.CharField(u'名称', max_length=64)
    description = models.CharField(u'描述', max_length=64, blank=True,null=True)
    ptype = models.PositiveSmallIntegerField('匹配类型', choices=((1, '头匹配'),(2, '正则匹配')) , default=1)
    
    class Meta:
        app_label = 'base'
        verbose_name = u'路由规则'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.name

class RoutePattern(models.Model):
    
    route = models.ForeignKey(Route, verbose_name="所属路由", related_name='patterns')
    content = models.CharField(u'匹配内容', max_length=128)
    
    class Meta:
        app_label = 'base'
        verbose_name = u'路由匹配内容'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.content


