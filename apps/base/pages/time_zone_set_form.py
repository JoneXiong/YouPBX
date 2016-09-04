# coding=utf-8

from django import forms

from xadmin.views.page import FormPage
from xadmin.sites import site
from xadmin import widgets
from xadmin.views.base import filter_hook


class TimeZone(FormPage):
    
    verbose_name = u'日期时区'
    
    def prepare_form(self):
        class MyForm(forms.Form):
            dt = forms.DateTimeField(label='新的时间')
            zone = forms.CharField(label='新的时区')
            
    @filter_hook
    def save_forms(self):
        pass