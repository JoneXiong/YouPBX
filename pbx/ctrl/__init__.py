# -*- coding: utf-8 -*-
import os


from mole.const import TEMPLATE_PATH

cur = os.path.split(os.path.realpath(__file__))[0]
templates_path = os.path.join(cur,'templates')
TEMPLATE_PATH.append(templates_path)

####### 自定义视图 #########
import routes
import interface
