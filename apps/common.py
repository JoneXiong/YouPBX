# coding=utf-8
from pbx import gen_xml
from pbx.rpc import in_api

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
        print '------------re xml'
        gen_xml.main()
        return in_api.reload_xml()
        