# -*- coding: utf-8 -*-

import datetime

from mocrud.extend import ObjectOp, ModelOp
import wtforms
from mocrud import ormfields
from mocrud.utils import flash

from ..models import Channels
import plivo_call

class Hangup(ObjectOp):
    verbose_name = u'挂断'
    pk = 'uuid'
    only_id = True
    
    def action(self, form, request):
        ids = request.forms.getall('id')
        for id in ids:
            plivo_call.hangup(id)
        flash(u'操作成功', 'success')
        return self.redirect()
    
class Dail(ModelOp):
    verbose_name = u'拨号'
    class OpForm(wtforms.Form):
        fr = wtforms.TextField(u'From', validators=[wtforms.validators.Required()])
        to = wtforms.TextField(u'To', validators=[wtforms.validators.Required()])
    
    def action(self, form, request):
        m_fr = form.fr.data.lstrip().rstrip()
        m_to = form.to.data.lstrip().rstrip()
        plivo_call.dail(m_fr,m_to)
        flash(u'拨打 %s 成功' %m_to, 'success')
        return self.redirect()
    
Channels.Admin.ops = [Hangup, Dail]