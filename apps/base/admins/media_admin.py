# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon
from xadmin import widgets

from apps.base import models
from apps.common import ReXmlAdmin


class MediaFileAdmin(ReXmlAdmin):

    model_icon = fa_icon('file-sound-o')
    list_display = ['comment','tag','file_size','show_true_path']
    menu_group = 'exten_group'
    app_label = 'funcs'
    list_per_page = 20

    def show_true_path(self,obj):
        return '<audio src="/static/sounds/%s" controls="controls">'%obj.true_path
    show_true_path.allow_tags = True
site.register(models.MediaFile, MediaFileAdmin)

class PhraseItemInline(object):
    model = models.PhraseItem
    extra = 0

    def get_field_attrs(self, db_field, **kwargs):
        attrs = super(PhraseItemInline, self).get_field_attrs(db_field, **kwargs)
        if db_field.name == 'sound_content':
            fkwidget = widgets.ForeignKeyPopupWidget(self,models.MediaFile,'true_path')
            charwidget = widgets.AdminTextInputWidget()
            attrs['widget'] = widgets.SelectRelation(self,'sound_type',{
                'audio':fkwidget,
                'tts': charwidget,
                'number': charwidget,
                'count': charwidget,
                'tts_var': charwidget,
                'number_var': charwidget,
                'count_var': charwidget,
            },inline_ref='items')
        return attrs

class PhraseMacroAdmin(object):
    app_label = 'funcs'
    order = 7
    inlines = [PhraseItemInline]
    menu_group = 'exten_group'
site.register(models.PhraseMacro, PhraseMacroAdmin)


