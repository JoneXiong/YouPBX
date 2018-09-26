# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon
from xadmin import widgets
from xadmin import layout
from xadmin.views import filter_hook

from apps.funcs import models
from apps.common import ReXmlAdmin
from apps.base import models as base_models


class ExtensionAdmin(ReXmlAdmin):
    app_label = 'funcs'
    menu_group = 'exten_group'
    list_display = ['desc','action_type','action_to_id']
    order = 7

    def get_field_attrs(self, db_field, **kwargs):
        attrs = super(ExtensionAdmin, self).get_field_attrs(db_field, **kwargs)
        if db_field.name == 'action_to_id':
            attrs['widget'] = widgets.SelectRelation(self,'action_type',{
                'device':widgets.ForeignKeyPopupWidget(self,models.Device,'id'),
                'ivr': widgets.ForeignKeyPopupWidget(self,models.IVR,'id'),
                'conference': widgets.ForeignKeyPopupWidget(self,models.Conference,'id'),
                #'queue': widgets.ForeignKeyPopupWidget(self,models.Queue,'id'),
                'voicemail': widgets.ForeignKeyPopupWidget(self,models.VoiceMail,'id'),
            })
        if db_field.name == 'sound_content':
            fkwidget = widgets.ForeignKeyPopupWidget(self,base_models.MediaFile,'true_path')
            charwidget = widgets.AdminTextInputWidget()
            attrs['widget'] = widgets.SelectRelation(self,'sound_type',{
                'audio':fkwidget,
                'tts': charwidget,
                'number': charwidget,
                'count': charwidget,
                'tts_var': charwidget,
                'number_var': charwidget,
                'count_var': charwidget,
            })
        return attrs

site.register(models.Extension, ExtensionAdmin)

