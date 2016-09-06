# coding=utf-8

from xadmin import site

from apps.base import models
from apps.common import ReXmlAdmin


class NumberAdmin(ReXmlAdmin):
    
    menu_group = 'cat_group'
    order = 3

class NumberPool(ReXmlAdmin):
    
    menu_group = 'cat_group'
    order = 2

site.register(models.Number, NumberAdmin)
site.register(models.NumberPool, NumberPool)