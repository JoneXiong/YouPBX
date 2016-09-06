# coding=utf-8

from xadmin import site

from apps.base import models
from apps.common import ReXmlAdmin

class RoutePatternInline(object):
    model = models.RoutePattern
    extra = 0

class RouteAdmin(ReXmlAdmin):
    
    inlines = [ RoutePatternInline ]
    menu_group = 'trunk_group'
    order = 1

site.register(models.Route, RouteAdmin)
