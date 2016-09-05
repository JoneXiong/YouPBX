# coding=utf-8
from pbx import gen_xml
from pbx.rpc import in_api
from base.pages import FsConfInit

class ReXmlAdmin(object):
    
    def do_add(self):
        super(ReXmlAdmin,self).do_add()
        res = self._rexml()
        if res['code']!=0:
            return res['msg']
    
    def do_update(self):
        super(ReXmlAdmin,self).do_update()
        res = self._rexml()
        if res['code']!=0:
            return res['msg']
     
    def do_delete(self):
        super(ReXmlAdmin,self).do_delete()
        res = self._rexml()
        if res['code']!=0:
            return res['msg']
     
    def do_deletes(self, qs):
        super(ReXmlAdmin,self).do_deletes(qs)
        res = self._rexml()
        if res['code']!=0:
            return res['msg']
        
    def _rexml(self):
        fs_conf_path = FsConfInit.options('fs_conf_path')
        if fs_conf_path:
            gen_xml.gen_all(fs_conf_path)
            return in_api.reload_xml()
        else:
            return {'code': -10, 'msg': u'请先进行【FS系统配置】'}
        