# coding=utf-8

from plivo.core.freeswitch.inboundsocket import InboundEventSocket
from plivo.core.errors import ConnectError
from plivo.utils.logger import StdoutLogger


log = StdoutLogger()


def api(cmd, bg=False, ok_check=True):
    #global inbound_event_listener
    import event_socket
    inbound_event_listener = event_socket.inbound_event_listener
    data = {}
    if not inbound_event_listener:
        try:
            event_socket.connect()
        except ConnectError, e:
            return {'code': -9, 'msg': 'connect failed !', 'data': data}
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

def status():
    return api('status', ok_check=False)
        
def sofia_status():
    return api('sofia status', ok_check=False)

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

def call_spy(user,uuid):
    cmd = 'originate %s &eavesdrop(%s)'%(user, uuid)
    return api(cmd, bg=True)

def send_agent_status_change_event(agent_number,status,status_str):
    import event_socket
    from dao import agent_dao
    hander = event_socket.inbound_event_listener
    event = "CUSTOM\nEvent-Name: CUSTOM\nEvent-Subclass: oe::agent_status_change\n" 
    queues = agent_dao.get_agent_queues(agent_number)
    print 'agent %s in queues %s'%(agent_number,queues)
    param = {
        'Event-Name': 'CUSTOM',
        'Event-Subclass': 'oe::agent_status_change',
        'Agent': agent_number,
        'Agent-Status': status,
        'StatusStr': status_str,
        'Queues': ','.join(queues),
    }
    param_str = '\n'.join(['%s: %s'%(k,v) for k,v in param.items()])
    cmd = 'CUSTOM\n%s\n'%param_str
    hander.sendevent(cmd)
    #event_tpl = 'Event-Name=CUSTOM,Event-Subclass=oe::agent_status_change,Agent=%s,Agent-Status=%s,StatusStr=%s'
    #api('exec:event,'+ event_tpl%(agent_number,status,status_str))
