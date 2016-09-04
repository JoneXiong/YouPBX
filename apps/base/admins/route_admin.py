# coding=utf-8

from xadmin import site

from apps.base import models
from apps.common import ReXmlAdmin

class RoutePatternInline(object):
    model = models.RoutePattern
    extra = 0


class RouteAdmin(ReXmlAdmin):
    inlines = [ RoutePatternInline ]
    pass

site.register(models.Route, RouteAdmin)
# site.register(models.RoutePattern)