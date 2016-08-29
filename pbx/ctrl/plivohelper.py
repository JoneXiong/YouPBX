# -*- coding: utf-8 -*-

__VERSION__ = "v0.1"

import urllib, urllib2, base64, hmac
from hashlib import sha1
from xml.dom.minidom import Document

try:
    from google.appengine.api import urlfetch
    APPENGINE = True
except ImportError:
    APPENGINE = False
try:
    import json
except ImportError:
    import simplejson as json


class PlivoException(Exception): pass


# Plivo REST Helpers
# ===========================================================================

class HTTPErrorProcessor(urllib2.HTTPErrorProcessor):
    def https_response(self, request, response):
        code, msg, hdrs = response.code, response.msg, response.info()
        if code >= 300:
            response = self.parent.error(
                'http', request, response, code, msg, hdrs)
        return response

class HTTPErrorAppEngine(Exception): pass

class PlivoUrlRequest(urllib2.Request):
    def get_method(self):
        if getattr(self, 'http_method', None):
            return self.http_method
        return urllib2.Request.get_method(self)

class REST(object):
    """Plivo helper class for making
    REST requests to the Plivo API.  This helper library works both in
    standalone python applications using the urllib/urlib2 libraries and
    inside Google App Engine applications using urlfetch.
    """
    def __init__(self, url, auth_id='', auth_token='', api_version=__VERSION__):
        """initialize a object

        url: Rest API Url
        auth_id: Plivo SID/ID
        auth_token: Plivo token

        returns a Plivo object
        """
        self.url = url
        self.auth_id = auth_id
        self.auth_token = auth_token
        self.opener = None
        self.api_version = api_version

    def _build_get_uri(self, uri, params):
        if params:
            if uri.find('?') > 0:
                if uri[-1] != '&':
                    uri += '&'
                uri = uri + urllib.urlencode(params)
            else:
                uri = uri + '?' + urllib.urlencode(params)
        return uri

    def _urllib2_fetch(self, uri, params, method=None):
        # install error processor to handle HTTP 201 response correctly
        if self.opener == None:
            self.opener = urllib2.build_opener(HTTPErrorProcessor)
            urllib2.install_opener(self.opener)

        if method and method == 'GET':
            uri = self._build_get_uri(uri, params)
            req = PlivoUrlRequest(uri)
        else:
            req = PlivoUrlRequest(uri, urllib.urlencode(params))
            if method and (method == 'DELETE' or method == 'PUT'):
                req.http_method = method

        authstring = base64.encodestring('%s:%s' % (self.auth_id, self.auth_token))
        authstring = authstring.replace('\n', '')
        req.add_header("Authorization", "Basic %s" % authstring)

        response = urllib2.urlopen(req)
        return response.read()

    def _appengine_fetch(self, uri, params, method):
        if method == 'GET':
            uri = self._build_get_uri(uri, params)

        try:
            httpmethod = getattr(urlfetch, method)
        except AttributeError:
            raise NotImplementedError(
                "Google App Engine does not support method '%s'" % method)

        authstring = base64.encodestring('%s:%s' % (self.auth_id, self.auth_token))
        authstring = authstring.replace('\n', '')
        r = urlfetch.fetch(url=uri, payload=urllib.urlencode(params),
            method=httpmethod,
            headers={'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic %s' % authstring})
        if r.status_code >= 300:
            raise HTTPErrorAppEngine("HTTP %s: %s" % \
                (r.status_code, r.content))
        return r.content

    def request(self, path, method=None, data={}):
        """sends a request and gets a response from the Plivo REST API

        path: the URL (relative to the endpoint URL, after the /v1
        method: the HTTP method to use, defaults to POST
        data: for POST or PUT, a dict of data to send

        returns Plivo response in XML or raises an exception on error
        """
        if not path:
            raise ValueError('Invalid path parameter')
        if method and method not in ['GET', 'POST', 'DELETE', 'PUT']:
            raise NotImplementedError(
                'HTTP %s method not implemented' % method)

        if path[0] == '/':
            uri = self.url + path
        else:
            uri = self.url + '/' + path

        if APPENGINE:
            return json.loads(self._appengine_fetch(uri, data, method))
        return json.loads(self._urllib2_fetch(uri, data, method))

    def reload_config(self, call_params):
        """REST Reload Plivo Config helper
        """
        path = '/' + self.api_version + '/ReloadConfig/'
        method = 'POST'
        return self.request(path, method, call_params)

    def reload_cache_config(self, call_params):
        """REST Reload Plivo Cache Config helper
        """
        path = '/' + self.api_version + '/ReloadCacheConfig/'
        method = 'POST'
        return self.request(path, method, call_params)

    def call(self, call_params):
        """REST Call Helper
        """
        path = '/' + self.api_version + '/Call/'
        method = 'POST'
        return self.request(path, method, call_params)

    def bulk_call(self, call_params):
        """REST BulkCalls Helper
        """
        path = '/' + self.api_version + '/BulkCall/'
        method = 'POST'
        return self.request(path, method, call_params)

    def group_call(self, call_params):
        """REST GroupCalls Helper
        """
        path = '/' + self.api_version + '/GroupCall/'
        method = 'POST'
        return self.request(path, method, call_params)

    def transfer_call(self, call_params):
        """REST Transfer Live Call Helper
        """
        path = '/' + self.api_version + '/TransferCall/'
        method = 'POST'
        return self.request(path, method, call_params)

    def hangup_all_calls(self):
        """REST Hangup All Live Calls Helper
        """
        path = '/' + self.api_version + '/HangupAllCalls/'
        method = 'POST'
        return self.request(path, method)

    def hangup_call(self, call_params):
        """REST Hangup Live Call Helper
        """
        path = '/' + self.api_version + '/HangupCall/'
        method = 'POST'
        return self.request(path, method, call_params)

    def schedule_hangup(self, call_params):
        """REST Schedule Hangup Helper
        """
        path = '/' + self.api_version + '/ScheduleHangup/'
        method = 'POST'
        return self.request(path, method, call_params)

    def cancel_scheduled_hangup(self, call_params):
        """REST Cancel a Scheduled Hangup Helper
        """
        path = '/' + self.api_version + '/CancelScheduledHangup/'
        method = 'POST'
        return self.request(path, method, call_params)

    def record_start(self, call_params):
        """REST RecordStart helper
        """
        path = '/' + self.api_version + '/RecordStart/'
        method = 'POST'
        return self.request(path, method, call_params)

    def record_stop(self, call_params):
        """REST RecordStop
        """
        path = '/' + self.api_version + '/RecordStop/'
        method = 'POST'
        return self.request(path, method, call_params)

    def conference_mute(self, call_params):
        """REST Conference Mute helper
        """
        path = '/' + self.api_version + '/ConferenceMute/'
        method = 'POST'
        return self.request(path, method, call_params)

    def play(self, call_params):
        """REST Play something on a Call Helper
        """
        path = '/' + self.api_version + '/Play/'
        method = 'POST'
        return self.request(path, method, call_params)

    def play_stop(self, call_params):
        """REST PlayStop on a Call Helper
        """
        path = '/' + self.api_version + '/PlayStop/'
        method = 'POST'
        return self.request(path, method, call_params)

    def schedule_play(self, call_params):
        """REST Schedule playing something on a call Helper
        """
        path = '/' + self.api_version + '/SchedulePlay/'
        method = 'POST'
        return self.request(path, method, call_params)

    def cancel_scheduled_play(self, call_params):
        """REST Cancel a Scheduled Play Helper
        """
        path = '/' + self.api_version + '/CancelScheduledPlay/'
        method = 'POST'
        return self.request(path, method, call_params)

    def sound_touch(self, call_params):
        """REST Add soundtouch audio effects to a Call
        """
        path = '/' + self.api_version + '/SoundTouch/'
        method = 'POST'
        return self.request(path, method, call_params)

    def sound_touch_stop(self, call_params):
        """REST Remove soundtouch audio effects on a Call
        """
        path = '/' + self.api_version + '/SoundTouchStop/'
        method = 'POST'
        return self.request(path, method, call_params)

    def send_digits(self, call_params):
        """REST Send digits to a Call
        """
        path = '/' + self.api_version + '/SendDigits/'
        method = 'POST'
        return self.request(path, method, call_params)

    def conference_unmute(self, call_params):
        """REST Conference Unmute helper
        """
        path = '/' + self.api_version + '/ConferenceUnmute/'
        method = 'POST'
        return self.request(path, method, call_params)

    def conference_kick(self, call_params):
        """REST Conference Kick helper
        """
        path = '/' + self.api_version + '/ConferenceKick/'
        method = 'POST'
        return self.request(path, method, call_params)

    def conference_hangup(self, call_params):
        """REST Conference Hangup helper
        """
        path = '/' + self.api_version + '/ConferenceHangup/'
        method = 'POST'
        return self.request(path, method, call_params)

    def conference_deaf(self, call_params):
        """REST Conference Deaf helper
        """
        path = '/' + self.api_version + '/ConferenceDeaf/'
        method = 'POST'
        return self.request(path, method, call_params)

    def conference_undeaf(self, call_params):
        """REST Conference Undeaf helper
        """
        path = '/' + self.api_version + '/ConferenceUndeaf/'
        method = 'POST'
        return self.request(path, method, call_params)

    def conference_record_start(self, call_params):
        """REST Conference RecordStart helper
        """
        path = '/' + self.api_version + '/ConferenceRecordStart/'
        method = 'POST'
        return self.request(path, method, call_params)

    def conference_record_stop(self, call_params):
        """REST Conference RecordStop
        """
        path = '/' + self.api_version + '/ConferenceRecordStop/'
        method = 'POST'
        return self.request(path, method, call_params)

    def conference_play(self, call_params):
        """REST Conference Play helper
        """
        path = '/' + self.api_version + '/ConferencePlay/'
        method = 'POST'
        return self.request(path, method, call_params)

    def conference_speak(self, call_params):
        """REST Conference Speak helper
        """
        path = '/' + self.api_version + '/ConferenceSpeak/'
        method = 'POST'
        return self.request(path, method, call_params)

    def conference_list(self, call_params):
        """REST Conference List Helper
        """
        path = '/' + self.api_version + '/ConferenceList/'
        method = 'POST'
        return self.request(path, method, call_params)

    def conference_list_members(self, call_params):
        """REST Conference List Members Helper
        """
        path = '/' + self.api_version + '/ConferenceListMembers/'
        method = 'POST'
        return self.request(path, method, call_params)



# RESTXML Response Helpers
# ===========================================================================

class Element(object):
    """Plivo basic element object.
    """
    VALID_ATTRS = ()

    def __init__(self, **kwargs):
        self.name = self.__class__.__name__
        self.body = None
        self.nestables = ()
        self.elements = []
        self.attrs = {}
        for k, v in kwargs.items():
            if k == "sender":
                k = "from"
            self._is_valid_attribute(k)
            v = Element.bool2txt(v)
            if v is not None:
                self.attrs[k] = unicode(v)

    def _is_valid_attribute(self, attr):
        if not attr in self.VALID_ATTRS:
            raise PlivoException("Invalid attribute '%s' for Element %s" \
                % (attr, self.name))

    @staticmethod
    def bool2txt(var):
        """Map True to 'true'
        and False to 'false'
        else don't modify value
        """
        if var is True:
            return 'true'
        elif var is False:
            return 'false'
        return var

    def __repr__(self):
        """
        String representation of a element
        """
        doc = Document()
        return self._xml(doc).toxml()

    def _xml(self, root):
        """
        Return an XML element representing this element
        """
        element = root.createElement(self.name)

        # Add attributes
        keys = self.attrs.keys()
        keys.sort()
        for a in keys:
            element.setAttribute(a, self.attrs[a])

        if self.body:
            text = root.createTextNode(self.body)
            element.appendChild(text)

        for c in self.elements:
            element.appendChild(c._xml(root))

        return element

    @staticmethod
    def check_post_get_method(method=None):
        if not method in ('GET', 'POST'):
            raise PlivoException("Invalid method parameter, must be 'GET' or 'POST'")

    def append(self, element):
        if not self.nestables:
            raise PlivoException("%s is not nestable" % self.name)
        if not element.name in self.nestables:
            raise PlivoException("%s is not nestable inside %s" % \
                            (element.name, self.name))
        self.elements.append(element)
        return element

    def asUrl(self):
        return urllib.quote(str(self))

    def addSpeak(self, text, **kwargs):
        return self.append(Speak(text, **kwargs))

    def addPlay(self, url, **kwargs):
        return self.append(Play(url, **kwargs))

    def addWait(self, **kwargs):
        return self.append(Wait(**kwargs))

    def addRedirect(self, url=None, **kwargs):
        return self.append(Redirect(url, **kwargs))

    def addNotify(self, url=None, **kwargs):
        return self.append(Notify(url, **kwargs))

    def addSIPTransfer(self, url=None, **kwargs):
        return self.append(SIPTransfer(url, **kwargs))

    def addHangup(self, **kwargs):
        return self.append(Hangup(**kwargs))

    def addGetDigits(self, **kwargs):
        return self.append(GetDigits(**kwargs))

    def addGetSpeech(self, **kwargs):
        return self.append(GetSpeech(**kwargs))

    def addNumber(self, number, **kwargs):
        return self.append(Number(number, **kwargs))

    def addDial(self, **kwargs):
        return self.append(Dial(**kwargs))

    def addRecord(self, **kwargs):
        return self.append(Record(**kwargs))

    def addConference(self, name, **kwargs):
        return self.append(Conference(name, **kwargs))

    def addPreAnswer(self, **kwargs):
        return self.append(PreAnswer(**kwargs))


class Response(Element):
    """Plivo response object.

    version: Plivo API version v0.1
    """
    VALID_ATTRS = ()

    def __init__(self):
        Element.__init__(self)
        self.nestables = ('Speak', 'Play', 'GetDigits', 'Record', 'Dial',
            'Redirect', 'Notify', 'Wait', 'Hangup', 'PreAnswer', 'Conference', 'GetSpeech',
            'SIPTransfer')

class Speak(Element):
    """Speak text

    text: text to say
    voice: voice to be used based on TTS engine
    language: language to use
    loop: number of times to say this text
    """
    VALID_ATTRS = ('voice', 'language',
                   'loop', 'engine', 'type',
                   'method')

    def __init__(self, text, **kwargs):
        Element.__init__(self, **kwargs)
        self.body = text

class Play(Element):
    """Play audio file at a URL

    url: url of audio file, MIME type on file must be set correctly
    loop: number of time to say this text
    """
    VALID_ATTRS = ('loop',)
    def __init__(self, url, **kwargs):
        Element.__init__(self, **kwargs)
        self.body = url

class Wait(Element):
    """Wait for some time to further process the call

    length: length of wait time in seconds
    """
    VALID_ATTRS = ('length')
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)

class Redirect(Element):
    """Redirect call flow to another URL

    url: redirect url
    method: POST or GET (default POST)
    """
    VALID_ATTRS = ('method',)

    def __init__(self, url=None, **kwargs):
        Element.__init__(self, **kwargs)
        self.body = url

class Notify(Element):
    """Callback to a URL that this Element was executed (general purpose event)

    url: callback url
    method: POST or GET (default POST)
    """
    VALID_ATTRS = ('method',)

    def __init__(self, url=None, **kwargs):
        Element.__init__(self, **kwargs)
        self.body = url

class SIPTransfer(Element):
    """SIPTransfer

    url: sip uris 
    """
    VALID_ATTRS = ()

    def __init__(self, url=None, **kwargs):
        Element.__init__(self, **kwargs)
        self.body = url

class Hangup(Element):
    """Hangup the call
    """
    VALID_ATTRS = ('schedule', 'reason')

    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)

class GetDigits(Element):
    """Get digits from the caller's keypad

    action: URL to which the digits entered will be sent
    method: submit to 'action' url using GET or POST
    numDigits: how many digits to gather before returning
    timeout: wait for this many seconds before retry or returning
    finishOnKey: key that triggers the end of caller input
    retries: number of tries to execute all says and plays one by one
    playBeep: play a beep after all plays and says finish
    validDigits: digits which are allowed to be pressed
    invalidDigitsSound: Sound played when invalid digit pressed
    """
    VALID_ATTRS = ('action', 'method', 'timeout', 'finishOnKey',
                   'numDigits', 'retries', 'invalidDigitsSound',
                   'validDigits', 'playBeep')

    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        self.nestables = ('Speak', 'Play', 'Wait')


class GetSpeech(Element):
    """Get speech from the caller

    action: URL to which the detected speech will be sent
    method: submit to 'action' url using GET or POST
    timeout: wait for this many seconds before returning
    playBeep: play a beep after all plays and says finish
    engine: engine to be used by detect speech
    grammar: grammar to load
    """
    VALID_ATTRS = ('action', 'method', 'timeout', 
                   'engine', 'grammar', 'playBeep', 'grammarPath')

    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        self.nestables = ('Speak', 'Play', 'Wait')


class Number(Element):
    """Specify phone number in a nested Dial element.

    number: phone number to dial
    sendDigits: key to press after connecting to the number
    """
    VALID_ATTRS = ('sendDigits', 'sendOnPreanswer', 'gateways', 'gatewayCodecs',
                   'gatewayTimeouts', 'gatewayRetries', 'extraDialString')
    def __init__(self, number, **kwargs):
        Element.__init__(self, **kwargs)
        self.body = number

class Conference(Element):
    """Enter a conference room.

    room: room name

    waitSound: sound to play while alone in conference
          Can be a list of sound files separated by comma.
          (default no sound)
    muted: enter conference muted
          (default false)
    startConferenceOnEnter: the conference start when this member joins
          (default true)
    endConferenceOnExit: close conference after all members
            with this attribute set to 'true' leave. (default false)
    stayAlone: if 'false' and member is alone, conference is closed and member kicked out
          (default true)
    maxMembers: max members in conference
          (0 for max : 200)
    enterSound: sound to play when a member enters
          if empty, disabled
          if 'beep:1', play one beep
          if 'beep:2', play two beeps
          (default disabled)
    exitSound: sound to play when a member exits
          if empty, disabled
          if 'beep:1', play one beep
          if 'beep:2', play two beeps
          (default disabled)
    timeLimit: max time in seconds before closing conference
          (default 0, no timeLimit)
    hangupOnStar: exit conference when member press '*'
          (default false)
    recordFilePath: path where recording is saved.
        (default "" so recording wont happen)
    recordFileFormat: file format in which recording tis saved
        (default mp3)
    recordFileName: By default empty, if provided this name will be used for the recording
        (any unique name)
    action: redirect to this URL after leaving conference
    method: submit to 'action' url using GET or POST
    callbackUrl: url to request when call enters/leaves conference
            or has pressed digits matching (digitsMatch)
    callbackMethod: submit to 'callbackUrl' url using GET or POST
    digitsMatch: a list of matching digits to send with callbackUrl
            Can be a list of digits patterns separated by comma.
    floorEvent: 'true' or 'false'. When this member holds the floor,
                send notification to callbackUrl. (default 'false')
    """
    VALID_ATTRS = ('muted','beep','startConferenceOnEnter',
                   'endConferenceOnExit','waitSound','enterSound', 'exitSound',
                   'timeLimit', 'hangupOnStar', 'maxMembers', 'recordFilePath',
                   'recordFileFormat', 'recordFileName', 'action', 'method',
                   'digitsMatch', 'callbackUrl', 'callbackMethod', 
                   'stayAlone', 'floorEvent')

    def __init__(self, room, **kwargs):
        Element.__init__(self, **kwargs)
        self.body = room

class Dial(Element):
    """Dial another phone number and connect it to this call

    action: submit the result of the dial and redirect to this URL 
    method: submit to 'action' url using GET or POST
    hangupOnStar: hangup the b leg if a leg presses start and this is true
    callerId: caller id to be send to the dialed number
    callerName: caller name to be send to the dialed number
    timeLimit: hangup the call after these many seconds. 0 means no timeLimit
    confirmSound: Sound to be played to b leg before call is bridged
    confirmKey: Key to be pressed to bridge the call.
    dialMusic: Play music to a leg while doing a dial to b leg
                Can be a list of files separated by comma
    redirect: if 'false', don't redirect to 'action', only request url 
        and continue to next element. (default 'true')
    callbackUrl: url to request when bridge starts and bridge ends
    callbackMethod: submit to 'callbackUrl' url using GET or POST
    """
    VALID_ATTRS = ('action','method','timeout','hangupOnStar',
                   'timeLimit','callerId', 'callerName', 'confirmSound',
                   'dialMusic', 'confirmKey', 'redirect',
                   'callbackUrl', 'callbackMethod', 'digitsMatch')

    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        self.nestables = ('Number',)

class Record(Element):
    """Record audio from caller

    action: submit the result of the record to this URL
    method: submit to 'action' url using GET or POST
    maxLength: maximum number of seconds to record (default 60)
    timeout: seconds of silence before considering the recording complete (default 500)
    playBeep: play a beep before recording (true/false, default true)
    format: file format (default mp3)
    filePath: complete file path to save the file to
    finishOnKey: Stop recording on this key
    fileName: filename to be used for recording of file
    bothLegs: record both legs (true/false, default false)
              no beep will be played
    redirect: if 'false', don't redirect to 'action', only request url 
        and continue to next element. (default 'true')
    """
    VALID_ATTRS = ('action', 'method', 'timeout','finishOnKey',
                   'maxLength', 'bothLegs', 'playBeep',
                   'fileFormat', 'filePath', 'fileName', 'redirect')

    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)

class PreAnswer(Element):
    """Answer the call in Early Media Mode and execute nested element
    """
    VALID_ATTRS = ()

    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        self.nestables = ('Play', 'Speak', 'GetDigits', 'Wait', 'GetSpeech', 'Redirect', 'Notify', 'SIPTransfer')


# Plivo Utility function and Request Validation
# ===========================================================================

class Utils(object):
    def __init__(self, auth_id='', auth_token=''):
        """initialize a plivo utility object

        auth_id: Plivo account SID/ID
        auth_token: Plivo account token

        returns a Plivo util object
        """
        self.auth_id = auth_id
        self.auth_token = auth_token

    def validateRequest(self, uri, postVars, expectedSignature):
        """validate a request from plivo

        uri: the full URI that Plivo requested on your server
        postVars: post vars that Plivo sent with the request
        expectedSignature: signature in HTTP X-Plivo-Signature header

        returns true if the request passes validation, false if not
        """

        # append the POST variables sorted by key to the uri
        s = uri
        for k, v in sorted(postVars.items()):
            s += k + v

        # compute signature and compare signatures
        return (base64.encodestring(hmac.new(self.auth_token, s, sha1).digest()).\
            strip() == expectedSignature)
