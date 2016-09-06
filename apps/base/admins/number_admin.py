# coding=utf-8

from xadmin import site

from apps.base import models
from apps.common import ReXmlAdmin


class NumberAdmin(ReXmlAdmin):
    pass

site.register(models.Number, NumberAdmin)
site.register(models.NumberPool, ReXmlAdmin)