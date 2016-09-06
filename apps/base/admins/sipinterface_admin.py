# coding=utf-8

from xadmin import site

from apps.base import models
from apps.common import ReXmlAdmin


class SipInterfaceAdmin(ReXmlAdmin):
    
    def get_nav_btns(self):
        return [
            '''<a href="/xadmin/page/sipinterfaceautoconf/" class="btn btn-primary"><i class="fa fa-inbox"></i> 自动检测</a> '''
        ]

site.register(models.SipInterface, SipInterfaceAdmin)