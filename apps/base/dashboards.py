# coding=utf-8
import datetime

from django.views.decorators.cache import never_cache

from xadmin.utils import fa_icon
from xadmin import site
from xadmin.views.website import IndexView

from apps.base import models
from . import html_widget

### 站点首页设置 ### 
class MainDashboard(object):

    widget_customiz = False

    def make_widgets(self):
        widgets = [
            [
                {"type": "html_pbx_status", "title": "软交换服务状态"},
                {"type": "chart", "model": "base.numberpool", 'chart': 'number_count'},
            ],
            [
                {"type": "qbutton", "title": "快速上手", "btns": [{'title': "FS系统配置",'icon': fa_icon('cog'), 'url': "/xadmin/page/fsconf/"}, {'model': models.SipInterface}, {'model': models.Location}, {'title': "官方主页",'icon': fa_icon('github'), 'url': "https://github.com/JoneXiong/YouPBX"}]},
                {"type": "html_sofia_status", "title": "VoIP状态"},
            ]
        ]
        self.widgets = widgets

    @never_cache
    def get(self, request, *args, **kwargs):
        self.make_widgets()
        self.widgets = self.get_widgets()
        return self.template_response(self.template, self.get_context())

site.register(IndexView, MainDashboard)
