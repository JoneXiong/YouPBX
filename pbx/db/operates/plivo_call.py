# -*- coding: utf-8 -*-

import plivohelper
REST_API_URL = 'http://127.0.0.1:8088'
API_VERSION = 'v0.1'

CALLBACK_URL_BASE = 'http://127.0.0.1:8070'

SID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
AUTH_TOKEN = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

extra_dial_string = "bridge_early_media=true,hangup_after_bridge=false"

plivo = plivohelper.REST(REST_API_URL, SID, AUTH_TOKEN, API_VERSION)


def dail(from_number, to_number):
    u'''
    拨通 A 到 B 的电话
    to outbound a single call
    '''
    call_params = {
        'From': from_number, # Caller Id
        'To' : to_number, # User Number to Call
        'Gateways' : "user/,user/", # Gateway string to try dialing separated by comma. First in list will be tried first
        'GatewayCodecs' : "'PCMA,PCMU','PCMA,PCMU'", # Codec string as needed by FS for each gateway separated by comma
        'GatewayTimeouts' : "20,20",      # Seconds to timeout in string for each gateway separated by comma
        'GatewayRetries' : "2,1", # Retry String for Gateways separated by comma, on how many times each gateway should be retried
        'ExtraDialString' : extra_dial_string,
        'AnswerUrl' : "http://127.0.0.1:8070/ctrl/answered/bridge/",
        'HangupUrl' : "http://127.0.0.1:8070/ctrl/hangup/",
        'RingUrl' : "http://127.0.0.1:8070/ctrl/ringing/",
    #    'TimeLimit' : '10',
    #    'HangupOnRing': '10',
    }
    result = plivo.call(call_params)
    return result

def hangup(call_uuid):
    u'''
    挂断某个电话
    Hangup call via Rest API
    '''
    hangup_call_params = {
        'CallUUID' : call_uuid,
    }
    return plivo.hangup_call(hangup_call_params)

def bulk_call(from_number, to_number_list):
    u'''
    to outbound several calls simultaneously
    '''
    call_params = {
        'Delimiter' : '>', # Delimter for the bulk list
        'From': from_number, # Caller Id
        'To' : '>'.join(to_number_list), # User Numbers to Call separated by delimeter
        'Gateways' : "user/>user/", # Gateway string for each number separated by delimeter
        'GatewayCodecs' : "'PCMA,PCMU'>'PCMA,PCMU'", # Codec string as needed by FS for each gateway separated by delimeter
        'GatewayTimeouts' : "60>30", # Seconds to timeout in string for each gateway separated by delimeter
        'GatewayRetries' : "2>1", # Retry String for Gateways separated by delimeter, on how many times each gateway should be retried
        'ExtraDialString' : extra_dial_string,
        'AnswerUrl' : "http://127.0.0.1:8070/ctrl/answered/bridge/",
        'HangupUrl' : "http://127.0.0.1:8070/ctrl/hangup/",
        'RingUrl' : "http://127.0.0.1:8070/ctrl/ringing/",
    #    'TimeLimit' : '10>30',
    #    'HangupOnRing': '0>0',
    }
    result = plivo.bulk_call(call_params)
    return result

def transfer():
    u'''
    Call Transfer
    '''
    transfer_call_params = {
        'Url' : "http://127.0.0.1:5000/transfered/",
        'CallUUID' : call_uuid, # CallUUID to transfer
    }
    res = plivo.transfer_call(transfer_call_params)
    return res

def valid_server():
    u'''
    Validate the request from server
    '''
    # the URL and POST parameters would normally be provided by the web framework
    url = "http://UUUUUUUUUUUUUUUUUU"
    postVars = {}
    
    # the request from Server also includes the HTTP header: X-REST-Signature
    # containing the expected signature
    signature = "SSSSSSSSSSSSSSSSSSSSSSSSSSSS"
    res = utils.validateRequest(url, postVars, signature)   # True False
    return res

def sound_touch(calluuid, direction='out'):
    u'''
    To add audio effects on a Call
    '''
    call_params = {'CallUUID':calluuid, 'AudioDirection':direction,
                   'PitchSemiTones': '', 'PitchOctaves': '', 'Pitch': '',
                   'Rate': '', 'Tempo': ''}
    res = plivo.sound_touch(call_params)
    return res

def sound_touch_stop(calluuid):
    call_params = {'CallUUID':calluuid}
    res = plivo.sound_touch_stop(call_params)
    return res

def send_digits(calluuid, digits, leg='aleg'):
    call_params = {'CallUUID':calluuid, 'Digits':digits, 'Leg':leg}
    res = plivo.send_digits(call_params)
    return res