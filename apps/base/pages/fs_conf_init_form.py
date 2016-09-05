# coding=utf-8

from django import forms

from xadmin.views.page import ConfigFormPage
from xadmin.sites import site
from xadmin import widgets
from xadmin.views.base import filter_hook

from apps.base import models
from pbx import init


class FsConfInit(ConfigFormPage):
    
    verbose_name = u'FS系统配置'
    app_label = 'base'
    #hidden_menu = True
    
    def prepare_form(self):
        class MyForm(forms.Form):
            fs_conf_path = forms.CharField(label='conf 路径')
            fs_sounds_path = forms.CharField(label='sounds 路径', required=False)
            fs_db_path = forms.CharField(label='db 路径', required=False)
        self.view_form = MyForm
            
    @filter_hook
    def save_forms(self):
        super(FsConfInit,self).save_forms()
        init.xml_init(self.options('fs_conf_path'))
    
site.register_page(FsConfInit)