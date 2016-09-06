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