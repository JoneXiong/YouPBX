# coding=utf-8

from xadmin import site

from apps.base import models
from apps.common import ReXmlAdmin


class ContextAdmin(ReXmlAdmin):
    
    menu_group = 'cat_group'
    order = 1

site.register(models.Context, ContextAdmin)

class LocationAdmin(ReXmlAdmin):
    
    menu_group = 'network_group'
    order = 2

site.register(models.Location, LocationAdmin)
site.register(models.MediaFile, ReXmlAdmin)


import route_admin
import trunk_admin
import netlist_admin
import number_admin
import sipinterface_admin