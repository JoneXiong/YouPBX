# coding=utf-8
import time
import threading

from plivo.core.freeswitch.inboundsocket import InboundEventSocket
from plivo.core.errors import ConnectError
from plivo.utils.logger import StdoutLogger

from config import event_socket_conf as conf

inbound_event_listener = None

class MyEventSocket(InboundEventSocket):

    def __init__(self, host, port, password, filter="ALL", log=None):
        InboundEventSocket.__init__(self, host, port, password, filter)
        self.log = log or StdoutLogger()

    def on_start_outcall(self):
        pass

    def on_end_outcall(self):
        pass

    def on_start_incall(self):
        pass

    def on_end_incall(self):
        pass

    def on_CHANNEL_BRIDGE(self,event):
        if event['variable_direction']=='inbound':
            number = event['Caller-Caller-ID-Number']
            uuid = event['variable_call_uuid']
            print '--- CHANNEL_BRIDGE:',number
            #print event
            from defs import VOIP_STATUS
            from long_conn import set_voip_status
            set_voip_status(number,VOIP_STATUS.calling,uuid)

    def on_CHANNEL_UNBRIDGE(self,event):
        if event['variable_direction']=='inbound':
            number = event['Caller-Caller-ID-Number']
            print '--- CHANNEL_UNBRIDGE:',number
            #print event
            from defs import VOIP_STATUS
            from long_conn import set_voip_status
            set_voip_status(number,VOIP_STATUS.idle)

    def on_custom(self, event):
        if event['Event-Subclass'] == 'oe::agent_status_change':
            print 'get custom event'

    def on_presence_in(self, event):
        import long_conn
        number = event['from'].split('@')[0]

        class reg_notify_thread(threading.Thread):
            def __init__(self, number, interval=None):
                threading.Thread.__init__(self)
                self.interval = interval
                self.number = number

            def run(self):
                if self.interval:time.sleep(self.interval)
                long_conn.send_reg_change_notify(int(self.number))

        th = reg_notify_thread(number, interval=1)
        th.start()


def connect():
    global inbound_event_listener
    inbound_event_listener = MyEventSocket(conf['host'], conf['port'], conf['pwd'])
    try:
        inbound_event_listener.connect()
    except ConnectError, e:
        inbound_event_listener.log.error("EventSocket connect failed: %s" % str(e))
        raise SystemExit('exit')
