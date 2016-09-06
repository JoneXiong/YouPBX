# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon

from apps.funcs import models
from apps.common import ReXmlAdmin

class DeviceAdmin(ReXmlAdmin):

    app_label = 'funcs'
    menu_group = 'application_group'
    order = 1
    model_icon = fa_icon('phone')
    
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
site.register(models.Device, DeviceAdmin)

site.register(models.TimeRoutes, TimeRoutesAdmin)
site.register(models.VoiceMail, VoiceMailAdmin)

import autoattendant_admin
import ringgroup_admin