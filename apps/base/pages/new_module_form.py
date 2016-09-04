# coding=utf-8

from django import forms

from xadmin.views.page import FormPage
from xadmin.sites import site
from xadmin import widgets
from xadmin.views.base import filter_hook

from apps.base import models


class NewModule(FormPage):
    
    verbose_name = u'装载模块'
    
    def prepare_form(self):
        class MyForm(forms.Form):
            media_file = forms.FileField(label='上传模块文件')
            if_load = forms.BooleanField(label='是否立即加载', required=False)
            
    @filter_hook
    def save_forms(self):
        pass
    