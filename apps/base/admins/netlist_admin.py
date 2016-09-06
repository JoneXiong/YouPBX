# coding=utf-8
'''
Access Control List
acl.conf
https://freeswitch.org/confluence/display/FREESWITCH/ACL
'''

from xadmin import site

from apps.base import models
from apps.common import ReXmlAdmin


class NetlistItemInline(object):
    model = models.NetlistItem
    extra = 0


class NetlistAdmin(ReXmlAdmin):
    
    inlines = [ NetlistItemInline ]
    menu_group = 'network_group'
    order = 3

site.register(models.Netlist, NetlistAdmin)