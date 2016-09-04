# coding=utf-8

from xadmin import site

from apps.base import models
from apps.common import ReXmlAdmin

site.register(models.Context)
site.register(models.Location)
site.register(models.MediaFile)
site.register(models.Netlist)
site.register(models.NetlistItem)

class NumberAdmin(ReXmlAdmin):
    pass

site.register(models.Number, NumberAdmin)
site.register(models.NumberPool)

site.register(models.SipInterface)


import route_admin
import trunk_admin
