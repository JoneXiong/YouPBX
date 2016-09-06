# coding=utf-8

from xadmin import site

from apps.funcs import models
from apps.common import ReXmlAdmin


site.register(models.Conference, ReXmlAdmin)
site.register(models.Device, ReXmlAdmin)

site.register(models.TimeRoutes, ReXmlAdmin)
site.register(models.VoiceMail, ReXmlAdmin)