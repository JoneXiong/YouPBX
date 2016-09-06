# coding=utf-8

from xadmin import site

from apps.base import models
from apps.common import ReXmlAdmin


class NetlistItemInline(object):
    model = models.NetlistItem
    extra = 0


class NetlistAdmin(ReXmlAdmin):
    inlines = [ NetlistItemInline ]
    pass

site.register(models.Netlist, NetlistAdmin)