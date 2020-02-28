# coding=utf-8

from django import forms
from django.http import HttpResponseRedirect


from xadmin.views.page import ConfigFormPage
from xadmin.sites import site
from xadmin import widgets
from xadmin.views.base import filter_hook

from apps.base import models
from pbx import init


class FsConf(ConfigFormPage):

    verbose_name = u'FS系统配置'
    app_label = 'base'
    #hidden_menu = True
    key = 'FsConf'

    def prepare_form(self):
        class MyForm(forms.Form):
            fs_conf_path = forms.CharField(label='conf 路径')
            fs_sounds_path = forms.CharField(label='sounds 路径', required=False)
            fs_db_path = forms.CharField(label='db 路径', required=False)
            fs_xml_init = forms.BooleanField(label='点保存时执行FS Config初始化', initial=False, required=False)
        self.view_form = MyForm

    @filter_hook
    def save_forms(self):
        super(FsConf,self).save_forms()
        data = self.form_obj.cleaned_data
        if data.get('fs_xml_init'):
            init.fs_conf_dir_init(self.options('fs_conf_path'))
            self.message_user('操作成功，且FS Config已初始化', 'success')
            return HttpResponseRedirect('/xadmin/page/fsconf/')

    def get_initial_data(self):
        ret = super(FsConf, self).get_initial_data()
        ret['fs_xml_init'] = False
        return ret

    def get_nav_btns(self):
        return [
            '''<a href="/xadmin/page/syncxml/?_redirect=/xadmin/page/fsconf/" class="btn btn-primary"><i class="fa fa-inbox"></i> 同步数据到FS</a> '''
        ]

site.register_page(FsConf)
