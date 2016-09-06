# coding=utf-8

from xadmin import site

from apps.funcs import models
from apps.common import ReXmlAdmin


class RingGroupDeviceInline(object):
    model = models.RingGroupDevice
    extra = 0

class RingGroupAdmin(ReXmlAdmin):
    inlines = [ RingGroupDeviceInline ]
    pass

site.register(models.RingGroup, RingGroupAdmin)