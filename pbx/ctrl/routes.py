# -*- coding: utf-8 -*-

from mole import route
from mole import request
from mole import response
from mole import redirect
from mole.template import jinja2_template

@route('/ctrl/',name='index')
def index():
    return 'ok'