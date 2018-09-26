# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon
from xadmin import widgets

from apps.base import models
from apps.common import ReXmlAdmin


class LocationAdmin(ReXmlAdmin):

    menu_group = 'network_group'
    order = 2
    model_icon = fa_icon('location-arrow')

site.register(models.Location, LocationAdmin)
