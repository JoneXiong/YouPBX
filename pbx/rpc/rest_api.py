# coding=utf-8

import plivohelper

import config


REST_API_URL = 'http://127.0.0.1:8088'
API_VERSION = 'v0.1'

CALLBACK_URL_BASE = 'http://127.0.0.1:%s'%config.main_server_conf['port']

SID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
AUTH_TOKEN = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

extra_dial_string = "bridge_early_media=false,hangup_after_bridge=true"

plivo = plivohelper.REST(REST_API_URL, SID, AUTH_TOKEN, API_VERSION)

def dail(from_number, to_number,userkey=None):
    u'''
    to outbound a single call
    '''
    from_info = from_number.split('|')
    to_info = to_number.split('|')
    call_params = {
        'From': from_info[1], # Caller Id
        'To' : to_info[1], # User Number to Call
        'AnswerUrl' : CALLBACK_URL_BASE+ "/rest/answer_notify/",
        'Gateways' : "%s"%(from_info[0]), # Gateway string to try dialing separated by comma. First in list will be tried first
        #'GatewayCodecs' : "'PCMA,PCMU','PCMA,PCMU'", # Codec string as needed by FS for each gateway separated by comma
        #'GatewayTimeouts' : "20,20",      # Seconds to timeout in string for each gateway separated by comma
        'GatewayRetries' : "1", # Retry String for Gateways separated by comma, on how many times each gateway should be retried
        'ExtraDialString' : extra_dial_string + ',plivo_userkey=%s'%userkey or "' '",
        'HangupUrl' : CALLBACK_URL_BASE+ "/rest/hangup_notify/",
        'RingUrl' : CALLBACK_URL_BASE+ "/rest/ring_notify/",
        #'TimeLimit' : '10',
    #    'HangupOnRing': '10',
    }
    result = plivo.call(call_params)
    return result


def hangup(calluuid):
    params = {
        'CallUUID': calluuid,
    }
    result = plivo.hangup_call(params)
    return result


