# coding=utf-8

from xadmin import site

from apps.base import models
from apps.common import ReXmlAdmin

class TrunkRoutePatternInline(object):
    model = models.TrunkRoutePattern
    extra = 0


class TrunkAdmin(ReXmlAdmin):
    
    inlines = [ TrunkRoutePatternInline ]
    menu_group = 'trunk_group'
    order = 2

site.register(models.Trunk, TrunkAdmin)
