# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon

from apps.funcs import models
from apps.common import ReXmlAdmin


class TimeRoutesAdmin(ReXmlAdmin):

    app_label = 'funcs'
    menu_group = 'application_group'
    order = 6
    model_icon = fa_icon('calendar-times-o')

site.register(models.TimeRoutes, TimeRoutesAdmin)
