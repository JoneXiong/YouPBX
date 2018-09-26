# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon
from xadmin import widgets
from xadmin import layout
from xadmin.views import filter_hook
from xadmin.plugins.inline import Inline
from django.forms import HiddenInput

from apps.funcs import models
from apps.common import ReXmlAdmin
from apps.base import models as base_models


class IVRKeymappingInline(object):
    model = models.IVRKeymapping
    extra = 2
    style = 'table'

    def get_field_attrs(self, db_field, **kwargs):
        attrs = super(IVRKeymappingInline, self).get_field_attrs(db_field, **kwargs)
        if db_field.name == 'action_to_id':
            attrs['widget'] = widgets.SelectRelation(self,'action_type',{
                'device':widgets.ForeignKeyPopupWidget(self,models.Device,'name'),
                'ivr': widgets.ForeignKeyPopupWidget(self,models.IVR,'id'),
                'conference': widgets.ForeignKeyPopupWidget(self,models.Conference,'id'),
                #'queue': widgets.ForeignKeyPopupWidget(self,models.Queue,'id'),
                'voicemail': widgets.ForeignKeyPopupWidget(self,models.VoiceMail,'id'),
                'parent': HiddenInput()
            },inline_ref='keymappings')
        return attrs

class IVRAdmin(ReXmlAdmin):
    app_label = 'funcs'
    menu_group = 'exten_group'
    order = 7

    inlines = [ IVRKeymappingInline ]

    form_layout = [
        layout.Fieldset('基础信息',
                        'name',
                        layout.Row('registry_max_failures','extension_digits')),
        layout.Fieldset('提示音',
            layout.Row('greet_long_type', 'greet_long_content')),
        layout.Fieldset('短提示音',
            layout.Row('greet_short_type', 'greet_short_content')),
        layout.Fieldset('按键无效提示音',
            layout.Row('invalid_sound_type', 'invalid_sound_content')),
        layout.Fieldset('退出IVR提示音',
            layout.Row('exit_sound_type', 'exit_sound_content')),
        Inline(models.IVRKeymapping),
    ]


    def get_field_attrs(self, db_field, **kwargs):
        attrs = super(IVRAdmin, self).get_field_attrs(db_field, **kwargs)
        if db_field.name == 'greet_long_content':
            fkwidget = widgets.ForeignKeyPopupWidget(self,base_models.MediaFile,'true_path')
            charwidget = widgets.AdminTextInputWidget()
            attrs['widget'] = widgets.SelectRelation(self,'greet_long_type',{
                'audio':fkwidget,
                'tts': charwidget,
                'number': charwidget,
                'count': charwidget,
                'tts_var': charwidget,
                'number_var': charwidget,
                'count_var': charwidget,
            })
        if db_field.name == 'greet_short_content':
            fkwidget = widgets.ForeignKeyPopupWidget(self,base_models.MediaFile,'true_path')
            charwidget = widgets.AdminTextInputWidget()
            attrs['widget'] = widgets.SelectRelation(self,'greet_short_type',{
                'audio':fkwidget,
                'tts': charwidget,
                'number': charwidget,
                'count': charwidget,
                'tts_var': charwidget,
                'number_var': charwidget,
                'count_var': charwidget,
            })
        if db_field.name == 'invalid_sound_content':
            fkwidget = widgets.ForeignKeyPopupWidget(self,base_models.MediaFile,'true_path')
            charwidget = widgets.AdminTextInputWidget()
            attrs['widget'] = widgets.SelectRelation(self,'invalid_sound_type',{
                'audio':fkwidget,
                'tts': charwidget,
                'number': charwidget,
                'count': charwidget,
                'tts_var': charwidget,
                'number_var': charwidget,
                'count_var': charwidget,
            })
        if db_field.name == 'exit_sound_content':
            fkwidget = widgets.ForeignKeyPopupWidget(self,base_models.MediaFile,'true_path')
            charwidget = widgets.AdminTextInputWidget()
            attrs['widget'] = widgets.SelectRelation(self,'exit_sound_type',{
                'audio':fkwidget,
                'tts': charwidget,
                'number': charwidget,
                'count': charwidget,
                'tts_var': charwidget,
                'number_var': charwidget,
                'count_var': charwidget,
            })
        return attrs

site.register(models.IVR, IVRAdmin)


