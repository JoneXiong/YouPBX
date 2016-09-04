# coding=utf-8

from django import forms

from xadmin.views.page import FormPage
from xadmin.sites import site
from xadmin import widgets
from xadmin.views.base import filter_hook

from apps.base import models
from pbx import init


class FsConfInit(FormPage):
    
    verbose_name = u'FS系统配置'
    app_label = 'base'
    hidden_menu = True
    
    def prepare_form(self):
        class MyForm(forms.Form):
            pass
        self.view_form = MyForm
            
    @filter_hook
    def save_forms(self):
        data = self.form_obj.cleaned_data
        init.xml_init()
    
site.register_page(FsConfInit)