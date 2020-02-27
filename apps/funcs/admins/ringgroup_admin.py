# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon

from apps.funcs import models
from apps.common import ReXmlAdmin


class RingGroupDeviceInline(object):
    model = models.RingGroupDevice
    extra = 0

    style_fields = {'device': 'fk_raw'}

class RingGroupAdmin(ReXmlAdmin):
    inlines = [ RingGroupDeviceInline ]
    app_label = 'funcs'
    menu_group = 'application_group'
    order = 2
    model_icon = fa_icon('users')

    style_fields = {'number': 'fk_raw'}
    fk_url_param = { 'number': {'_p_numberpool': 4} }

site.register(models.RingGroup, RingGroupAdmin)
