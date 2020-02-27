# coding=utf-8
import os
import datetime

from xadmin import site
from xadmin.utils import fa_icon
from xadmin import widgets
from xadmin import layout
from xadmin.views import filter_hook

from apps.funcs import models
from apps.common import ReXmlAdmin


class ConferenceAdmin(ReXmlAdmin):

    app_label = 'funcs'
    menu_group = 'application_group'
    order = 4

class TimeRoutesAdmin(ReXmlAdmin):

    app_label = 'funcs'
    menu_group = 'application_group'
    order = 6
    model_icon = fa_icon('calendar-times-o')

class VoiceMailAdmin(ReXmlAdmin):

    app_label = 'funcs'
    menu_group = 'application_group'
    order = 5
    model_icon = fa_icon('envelope')

site.register(models.Conference, ConferenceAdmin)


site.register(models.TimeRoutes, TimeRoutesAdmin)
site.register(models.VoiceMail, VoiceMailAdmin)

#import autoattendant_admin
import ringgroup_admin
import device_admin
