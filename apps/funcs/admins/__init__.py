# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon

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

import ringgroup_admin
from . import device_admin
from . import extension_admin
from . import ivr_admin
