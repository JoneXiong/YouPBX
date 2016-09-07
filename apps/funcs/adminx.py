# coding=utf-8

from xadmin import site
from xadmin.views.dashboard import AppDashboard

class FuncsIndex(AppDashboard):
    app_label = 'funcs'
    #widget_customiz = False
    
site.register_appindex(FuncsIndex)

import admins
