# coding=utf-8

from django import forms

from xadmin.views.page import FormPage
from xadmin.sites import site
from xadmin import widgets
from xadmin.views.base import filter_hook
from pbx import init
from pbx import utils as pbx_utils

class SipInterfaceAutoConf(FormPage):
    
    verbose_name = u'自动检测'
    app_label = 'base'
    hidden_menu = True
    
    def prepare_form(self):
        res = pbx_utils.get_sipinterface_default_ip_list()
        _choices= [(e,e) for e in res]
        class MyForm(forms.Form):
            ips = forms.MultipleChoiceField(label='选择IP', choices=_choices)
        self.view_form = MyForm
            
    @filter_hook
    def save_forms(self):
        data = self.form_obj.cleaned_data
        ips = data.get('ips', [])
        if ips:
            for ip in ips:
                init.create_sipinterface_with_ip(ip)
                from apps.common import ReXmlAdmin
                ReXmlAdmin()._rexml()
    
site.register_page(SipInterfaceAutoConf)

class SipInterfaceCreateByIP(FormPage):
    
    verbose_name = u'通过IP创建'
    app_label = 'base'
    hidden_menu = True
    
    def prepare_form(self):
        class MyForm(forms.Form):
            ip = forms.CharField(label='填写IP')
        self.view_form = MyForm
            
    @filter_hook
    def save_forms(self):
        data = self.form_obj.cleaned_data
        ip = data.get('ip')
        if ip:
            init.create_sipinterface_with_ip(ip)
            from apps.common import ReXmlAdmin
            ReXmlAdmin()._rexml()
    
site.register_page(SipInterfaceCreateByIP)
