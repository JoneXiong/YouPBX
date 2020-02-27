# coding=utf-8
import time
import threading

from plivo.core.freeswitch.inboundsocket import InboundEventSocket
from plivo.core.errors import ConnectError

from config import event_socket_conf as conf

inbound_event_listener = None


def connect(inbound_event_class=None):
    global inbound_event_listener
    eventclass = inbound_event_class or InboundEventSocket
    inbound_event_listener = eventclass(conf['host'], conf['port'], conf['pwd'])
    try:
        inbound_event_listener.connect()
    except ConnectError, e:
        inbound_event_listener.log.error("EventSocket connect failed: %s" % str(e))
        raise e
        #raise SystemExit('exit')
