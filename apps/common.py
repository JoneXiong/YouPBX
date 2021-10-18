# coding=utf-8

import threading
import time
import requests
import json

from django.conf import settings

from pbx import conf
from base.pages import FsConf


class make_xml_thread(threading.Thread):
    def __init__(self, fs_conf_path, interval=None):
        threading.Thread.__init__(self)
        self.interval = interval
        self.fs_conf_path = fs_conf_path

    def run(self):
        if self.interval:time.sleep(self.interval)
        conf.gen_all(self.fs_conf_path)
        r = requests.get(settings.FS_AGW_URL +'/reloadxml')
        res = json.loads(r.text)

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
        fs_conf_path = FsConf.options('fs_conf_path')
        if fs_conf_path:
            th = make_xml_thread(fs_conf_path, interval=1)
            th.start()
            return {'code': 0}
        else:
            return {'code': -10, 'msg': u'请先进行【FS系统配置】'}


