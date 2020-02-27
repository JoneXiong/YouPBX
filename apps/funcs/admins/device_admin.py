# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon
from xadmin import widgets
from xadmin import layout
from xadmin.views import filter_hook

from apps.funcs import models
from apps.common import ReXmlAdmin

class DeviceAdmin(ReXmlAdmin):

    app_label = 'funcs'
    menu_group = 'application_group'
    order = 1
    model_icon = fa_icon('phone')
    #hide_other_field = True
    search_fields = ['name']

    form_layout = [
        layout.TabHolder(
            layout.Tab(
                '基本设置',
                'name','registry_ringtype','registry_timeout',
                css_id = 'tab1'
            ),
            layout.Tab(
                '高级设置',
                'class_type','context','location','sip_username','sip_password','callerid_internal_name','callerid_internal_number',
                'callerid_external_name','callerid_external_number','media_mode',
                'sip_caller_id_field','sip_cid_format','sip_invite_format','voicemail','registry_ignoreFWD',
                css_id = 'tab2'
            )
        )
        ]

    def do_add(self):
        from apps.base import models
        obj = self.new_obj
        _number = obj.name
        try:
            models.Number.objects.get(number=_number)
            return u'号码已经存在'
        except:
            nb = models.Number()
            nb.number = _number
            nb.numberpool_id = 1
            nb.save()
            obj.number_id = nb.id
            super(DeviceAdmin,self).do_add()

    @filter_hook
    def get_readonly_fields(self):
        if self.org_obj:
            return ['name']
        else:
            return []
site.register(models.Device, DeviceAdmin)


