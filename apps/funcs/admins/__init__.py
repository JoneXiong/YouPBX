# coding=utf-8

from xadmin import site

from apps.funcs import models
from apps.common import ReXmlAdmin


class AutoattendantKeymappingInline(object):
    model = models.AutoattendantKeymapping
    extra = 0


class AutoattendantAdmin(ReXmlAdmin):
    inlines = [ AutoattendantKeymappingInline ]
    pass

site.register(models.Autoattendant, AutoattendantAdmin)



class RingGroupDeviceInline(object):
    model = models.RingGroupDevice
    extra = 0

class RingGroupAdmin(ReXmlAdmin):
    inlines = [ RingGroupDeviceInline ]
    pass

site.register(models.RingGroup)


# site.register(models.Autoattendant)
# site.register(models.AutoattendantKeymapping)
site.register(models.Conference)
site.register(models.Device)
# site.register(models.RingGroup)
# site.register(models.RingGroupDevice)
site.register(models.TimeRoutes)
site.register(models.VoiceMail)