# coding=utf-8

from django import forms

from xadmin.views.page import FormPage
from xadmin import site
from xadmin.views.base import filter_hook

from pbx import conf
from pbx.rpc import in_api
from .fs_conf_form import FsConf


class SyncXml(FormPage):
    app_label = 'base'
    verbose_name = '同步数据到FS'
    hidden_menu = True
    perm = 'SyncXml'

    def save_forms(self):
        fs_conf_path = FsConf.options('fs_conf_path')
        conf.gen_all(fs_conf_path)
        in_api.reload_xml()

    @filter_hook
    def get_response(self):
        self.message_user('确定同步数据到FS Config?')
        return super(SyncXml, self).get_response()

site.register_page(SyncXml)
