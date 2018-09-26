# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon

from apps.funcs import models
from apps.common import ReXmlAdmin


class VoiceMailAdmin(ReXmlAdmin):

    app_label = 'funcs'
    menu_group = 'application_group'
    order = 5
    model_icon = fa_icon('envelope')

site.register(models.VoiceMail, VoiceMailAdmin)
