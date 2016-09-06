# coding=utf-8

from xadmin.utils import fa_icon

verbose_name = u'PBX'

menus = (
         ('network_group','网络配置', fa_icon('signal') ),
         ('cat_group','分组', fa_icon('group') ),
         ('trunk_group','中继路由', fa_icon('sitemap') ),
         ('application_group','应用', fa_icon('whatsapp') ),
         )