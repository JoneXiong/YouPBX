# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon
from xadmin import widgets

from apps.base import models
from apps.common import ReXmlAdmin


class ContextAdmin(ReXmlAdmin):

    menu_group = 'cat_group'
    order = 1
    model_icon = fa_icon('group')

site.register(models.Context, ContextAdmin)
