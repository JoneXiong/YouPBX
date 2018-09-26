# coding=utf-8

from conference_models import *
from device_models import *
from ringgroup_models import *
from timeroutes_models import *
from voicemail_models import *
from .extension_models import *
from .ivr_models import *


    

    
#class res_users(osv.osv):
#    _inherit = "res.users"
#    _description = "Users"
#    
#    _columns = {
#       'device_id': fields.many2one('fs.device', u'选择号码', required = True),
#    }
#    
#    _defaults = {
#    }
#    
#    def get_device_number(self, cr, uid):
#        """
#        """
#        ids = [uid]
#        user = self.browse(cr, uid, ids, context=[])[0]
#        if user.device_id:
#            return user.device_id.number_id.number
#        else:
#            return ''

    

    

    

    

    
#class fs_timeofday(common.pbx_model):
#    _name = 'fs.timeofday'
#    _description = u'工作时间路由'
#    _columns = {
#            'name': fields.char(u'名称', size=64, required = True, ),
#    }
