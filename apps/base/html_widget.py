# coding=utf-8
import requests
import base64
import json

from django.conf import settings

from xadmin.utils import fa_icon
from xadmin.views.dashwidget import HtmlWidget, widget_manager


@widget_manager.register
class PbxStatusWidget(HtmlWidget):
    '''
    软交换服务状态
    '''
    widget_type = 'html_pbx_status'
    widget_icon = fa_icon('laptop')

    def has_perm(self):
        return True

    def context(self, context):
        r = requests.get(settings.FS_AGW_URL + '/base_status')
        res = json.loads(r.text)
        if res['code']==0:
            content = ''
            lines = base64.b64decode(res['data']).split('\n')
            content += '<b>运行时间</b>：%s 分<hr/>'%lines[0].split('minutes,')[0].replace('UP ','').replace('years','年').replace('days','天').replace('hours','小时')
            content += '<b>总会话数</b>：%s<hr/>'%lines[2].split(' session')[0]
            content += '<b>会话详情</b>：当前 %s<hr/>'%lines[3].replace('session(s) - peak',' &nbsp;&nbsp峰值').replace(', last 5min',' &nbsp;&nbsp最近5分钟')
            content += '<b>当前/最大栈大小</b>：%s'%lines[-1].replace('Current Stack Size/Max','').replace('/',' / ')
            context['content'] = content
        else:
            context['content'] = '获取失败'

@widget_manager.register
class SofiaStatusWidget(HtmlWidget):
    '''
    VoIP状态
    '''
    widget_type = 'html_sofia_status'
    widget_icon = fa_icon('tty')

    def has_perm(self):
        return True

    def context(self, context):
        r = requests.get(settings.FS_AGW_URL + '/sofia_status')
        res = json.loads(r.text)
        if res['code']==0:
            context['content'] = '%s'%base64.b64decode(res['data']).replace('\n','<br/>')
        else:
            context['content'] = '获取失败'
