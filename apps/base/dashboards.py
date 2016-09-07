# coding=utf-8

from xadmin.utils import fa_icon
from xadmin.views.dashwidget import HtmlWidget, widget_manager
from xadmin import site
from xadmin.views.website import IndexView


@widget_manager.register
class PbxStatusWidget(HtmlWidget):
    widget_type = 'html_pbx_status'
    widget_icon = fa_icon('laptop')

    def has_perm(self):
        return True

    def context(self, context):
        from pbx.rpc import in_api
        res = in_api.status()
        if res['code']==0:
            context['content'] = '%s'%res['data']['body'].replace('\n','<br/>')
        else:
            context['content'] = '获取失败'
            
@widget_manager.register
class SofiaStatusWidget(HtmlWidget):
    widget_type = 'html_sofia_status'
    widget_icon = fa_icon('tty')

    def has_perm(self):
        return True

    def context(self, context):
        from pbx.rpc import in_api
        res = in_api.sofia_status()
        if res['code']==0:
            context['content'] = '%s'%res['data']['body'].replace('\n','<br/>')
        else:
            context['content'] = '获取失败'


### 站点首页设置 ### 
class MainDashboard(object):
    widgets = [
        [
            {"type": "html_pbx_status", "title": "服务状态"},
        ],
        [
            {"type": "html_sofia_status", "title": "VoIP状态"},
        ]
    ]
site.register(IndexView, MainDashboard)
