# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon

from apps.funcs import models
from apps.common import ReXmlAdmin


class AutoattendantKeymappingInline(object):
    model = models.AutoattendantKeymapping
    extra = 0


class AutoattendantAdmin(ReXmlAdmin):
    inlines = [ AutoattendantKeymappingInline ]
    app_label = 'funcs'
    menu_group = 'application_group'
    order = 3
    model_icon = fa_icon('list')

site.register(models.Autoattendant, AutoattendantAdmin)