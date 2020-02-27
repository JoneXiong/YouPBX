# coding=utf-8

from django.db import models
'''
location & domain
'''

class Location(models.Model):
    '''
    Domain
    '''
    location_name = models.CharField(u'名称', max_length=64)
    domain_name = models.CharField(u'域标识', max_length=64)

    class Meta:
        app_label = 'base'
        verbose_name = u'域(Location)'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return  '%s (%s)'%(self.location_name, self.domain_name)
