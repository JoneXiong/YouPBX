# coding=utf-8

from xadmin import site

from apps.base import models
from apps.common import ReXmlAdmin

class TrunkRoutePatternInline(object):
    model = models.TrunkRoutePattern
    extra = 0


class TrunkAdmin(ReXmlAdmin):
    inlines = [ TrunkRoutePatternInline ]
    pass

site.register(models.Trunk, TrunkAdmin)
# site.register(models.TrunkRoutePattern)