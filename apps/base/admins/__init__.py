# coding=utf-8

from xadmin import site

from apps.base import models

site.register(models.Context)
site.register(models.Location)
site.register(models.MediaFile)
site.register(models.Netlist)
site.register(models.NetlistItem)
site.register(models.Number)
site.register(models.NumberPool)
site.register(models.Route)
site.register(models.RoutePattern)
site.register(models.SipInterface)
site.register(models.Trunk)
site.register(models.TrunkRoutePattern)
