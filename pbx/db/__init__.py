# -*- coding: utf-8 -*-
import os

####### Crud 初始化 #######
from mocrud.api import setup,uncheck,create_tables
import models
import operates
setup(models)
uncheck()
#create_tables()

####### 自定义视图 #########
import routes

from mole.const import TEMPLATE_PATH
cur = os.path.split(os.path.realpath(__file__))[0]
templates_path = os.path.join(cur,'templates')
TEMPLATE_PATH.append(templates_path)