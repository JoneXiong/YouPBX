# coding=utf-8

from plivo.core.freeswitch.inboundsocket import InboundEventSocket
from plivo.core.errors import ConnectError
from plivo.utils.logger import StdoutLogger

from config import event_socket_conf as conf

log = StdoutLogger()
inbound_event_listener = None

def api(cmd, bg=False, ok_check=True):
    global inbound_event_listener
    data = {}
    if not inbound_event_listener:
        inbound_event_listener = InboundEventSocket(conf['host'], conf['port'], conf['pwd'], filter="BACKGROUND_JOB")
    if not inbound_event_listener.connected:
        try:
            inbound_event_listener.connect()
        except ConnectError, e:
            log.error("connect failed: %s" % str(e))
            return {'code': -9, 'msg': 'connect failed !', 'data': data}
    fs_bg_api_string = cmd
    if bg:
        bg_api_response = inbound_event_listener.bgapi(fs_bg_api_string)
    else:
        bg_api_response = inbound_event_listener.api(fs_bg_api_string)
    log.info(str(bg_api_response))
    log.info(bg_api_response.get_response())
    data['body'] = bg_api_response.get_response()
    if ok_check and not bg_api_response.is_success():
        return {'code': -1, 'msg': 'bgapi failed !', 'data': data}
    if bg:
        job_uuid = bg_api_response.get_job_uuid()
        if not job_uuid:
            return {'code': -2, 'msg': 'bgapi jobuuid not found !', 'data': data}
        else:
            data['job_uuid'] = job_uuid
    
    return {'code': 0, 'msg': 'success !', 'data': data}

def reload_xml():
    return api('reloadxml')

def status(ok_check=False):
    return api('status')
        
def sofia_status(ok_check=False):
    return api('sofia status')

def reload_acl():
    return api('reloadacl')

def reload_callcenter():
    return api('reload mod_callcenter')

def reload_profile():
    cmd = 'sofia profile xxx rescan reloadxml'
    return api(cmd)

def show_gateways():
    cmd = 'sofia profile xxx gwlist up'
    return api(cmd)

def show_regusers():
    cmd = 'sofia status profile xxx reg'
    return api(cmd)