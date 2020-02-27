# coding=utf-8

from xadmin import site
from xadmin.views.dashboard import AppDashboard
from django.utils.translation import ugettext as _
from xadmin.views.website import MainView
from django.forms.forms import BoundField
from xadmin.widgets import SelectRelation


site.site_title = 'YouPBX'
site.site_footer  = 'Oejia CopyRight'
site.menu_style = 'default'
site.head_fix = False
site.ext_ui = False

#import dashboards

class BaseIndex(AppDashboard):
    app_label = 'base'
    #widget_customiz = False

site.register_appindex(BaseIndex)

from . import dashboards
import admins
import pages
