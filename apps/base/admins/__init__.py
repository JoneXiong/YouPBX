# coding=utf-8

from xadmin import site

from apps.base import models
from apps.common import ReXmlAdmin

site.register(models.Context, ReXmlAdmin)
site.register(models.Location, ReXmlAdmin)
site.register(models.MediaFile, ReXmlAdmin)


import route_admin
import trunk_admin
import netlist_admin
import number_admin
import sipinterface_admin