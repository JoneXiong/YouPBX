# -*- coding: utf-8 -*-

from mole import route
from mole import request
from mole import response
from mole import redirect
from mole.template import jinja2_template as render_template

from mocrud.admin import admin
from mocrud.utils import flash
from mocrud.db import db
from wtforms import Form, TextField, DateField, validators

#from models import Channels
#import plivo_call

#@route('/db/dail/',name='admin.calls_dail',method=['GET', 'POST'])
#def dail():
#    self = admin.get_admin_for(Channels)
#    
#    class DailForm(Form):
#        fr = TextField(u'From', validators=[validators.Required()])
#        to = TextField(u'To', validators=[validators.Required()])
#
#    if request.method == 'POST':
#        form = DailForm(request.forms)
#        if form.validate():
#            m_fr = form.fr.data.lstrip().rstrip()
#            m_to = form.to.data.lstrip().rstrip()
#            plivo_call.dail(m_fr,m_to)
#            flash(u'拨打 %s 成功' %m_to, 'success')
#            return redirect('/admin/channels/')
#    else:
#        form = DailForm()
#        
#    return render_template('dail.html',
#        model_admin=self,
#        instance=None,
#        form=form,
#        **self.get_extra_context()
#    )
#    
#@route('/db/hangup/:pk/',name='admin.hangup',method=['GET', 'POST'])
#def hangup(pk):
#    self = admin.get_admin_for(Channels)
#    
##    try:
##        instance = self.get_object(pk)
##    except self.model.DoesNotExist:
##        abort(404)
#
#    if request.method == 'POST':
#        m_id = request.forms["id"]
#        plivo_call.hangup(pk)
#        flash(u'操作成功', 'success')
#        return redirect('/admin/channels/')
#    else:
#        pass
#
#    return render_template('hangup.html',
#        model_admin=self,
#        instance=pk,
#        **self.get_extra_context()
#    )