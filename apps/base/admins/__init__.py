# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon

from apps.base import models
from apps.common import ReXmlAdmin


class ContextAdmin(ReXmlAdmin):
    
    menu_group = 'cat_group'
    order = 1
    model_icon = fa_icon('group')

site.register(models.Context, ContextAdmin)

class LocationAdmin(ReXmlAdmin):
    
    menu_group = 'network_group'
    order = 2
    model_icon = fa_icon('location-arrow')

site.register(models.Location, LocationAdmin)


class MediaFileAdmin(ReXmlAdmin):
    
    model_icon = fa_icon('file-sound-o')

site.register(models.MediaFile, MediaFileAdmin)


import route_admin
import trunk_admin
import netlist_admin
import number_admin
import sipinterface_admin