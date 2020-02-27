# coding=utf-8

from xadmin import site

from apps.base import models
from apps.common import ReXmlAdmin


class NumberAdmin(ReXmlAdmin):
    
    menu_group = 'cat_group'
    order = 3
    #hidden_menu = True
    search_fields = ['number']

class NumberPool(ReXmlAdmin):
    
    menu_group = 'cat_group'
    order = 2
    
    data_charts = {
        "number_count": {'title': u"应用", "x-field": "name", "y-field": ("count",), "order": ('id',),
                                  "option": {
                                             "series": {"bars": {"align": "center", "barWidth": 0.6,'show':True}},
                                             "xaxis": {"aggregate": "sum", "mode": "categories"},
                                             },
                         },
    }

site.register(models.Number, NumberAdmin)
site.register(models.NumberPool, NumberPool)
