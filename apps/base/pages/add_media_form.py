# coding=utf-8

from django import forms

from xadmin.views.page import FormPage
from xadmin.sites import site
from xadmin import widgets
from xadmin.views.base import filter_hook

from apps.base import models


class AddMedia(FormPage):
    
    verbose_name = u'增加媒体文件'
    
    def prepare_form(self):
        class MyForm(forms.Form):
            name = forms.CharField(label='名称')
            parent = forms.IntegerField(label='父目录', required=False, widget=widgets.ForeignKeyPopupWidget(self, models.MediaFile, 'id'))
            number = forms.CharField(label='分机号', required=False, help='通过此分机号来接听并录音')
            media_file = forms.FileField(label='上传媒体文件', required=False)
            
    @filter_hook
    def save_forms(self):
        pass
    