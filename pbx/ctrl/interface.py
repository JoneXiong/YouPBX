# -*- coding: utf-8 -*-

from mole import route
from mole import request
from mole import response
from mole import redirect
from mole.template import jinja2_template

import plivohelper

"""
The following URLs are implemented:
    * /ringing/
    * /answered/
    * /hangup/
    * /phonemenu/
"""


web = {}
#############           0             1            2           3
web['default'] = ('receptionist','hours', 'location', 'duck')
web['location'] = ('receptionist','east-bay', 'san-jose', 'marin')


@route('/ctrl/ringing/', method=['GET', 'POST'])
def ringing():
    """ringing URL"""
    # Post params- 'to': ringing number, 'request_uuid': request id given at the time of api call
    print "We got a ringing notification"
    return "OK"

@route('/ctrl/hangup/', method=['GET', 'POST'])
def hangup():
    """hangup URL"""
    # Post params- 'request_uuid': request id given at the time of api call,
    #               'CallUUID': unique id of call, 'reason': reason of hangup
    print "We got a hangup notification"
    return "OK"


@route('/ctrl/heartbeat/', method=['GET', 'POST'])
def heartbeat():
    """Call Heartbeat URL"""
    print "We got a call heartbeat notification\n"

    if request.method == 'POST':
        print request.form
    else:
        print request.args

    return "OK"


@route('/ctrl/answered/', method=['GET', 'POST'])
def answered():
    # Post params- 'CallUUID': unique id of call, 'Direction': direction of call,
    #               'To': Number which was called, 'From': calling number,
    #               If Direction is outbound then 2 additional params:
    #               'ALegUUID': Unique Id for first leg,
    #               'ALegRequestUUID': request id given at the time of api call

    if request.method == 'POST':
        try:
            print "CallUUID: %s" % request.form['CallUUID']
        except:
            pass

        try:
            print "All POST Params: %s" % request.form
        except:
            pass
    else:
        try:
            print "CallUUID: %s" % request.args['CallUUID']
        except:
            pass

        try:
            print "All GET Params: %s" % request.args
        except:
            pass

    return phonemenu()

@route('/ctrl/answered/bridge/', method=['GET', 'POST'])
def answered_bridge():
    From = request.POST['From']
    to = request.POST['To']
    r = plivohelper.Response()
    g = r.addDial()
    g.addNumber(From, gateways="user/,user/")
    return jinja2_template('response_template.xml', response=r)

@route('/ctrl/answered/ivr/', method=['GET', 'POST'])
def answered_ivr():
    return phonemenu()

def get_ggtts_url(text):
    from urllib import urlencode
    my_dict = {'tl':'zh','ie':'UTF-8','q':text}#, 'total': 1, 'idx': 0,'textlen': len(text), 'prev': 'input'}
    return "http://translate.google.cn/translate_tts?%s"%urlencode(my_dict)
    

def do_end(r,again_dest, last_dest, with_again=True):
    g = r.addGetDigits(numDigits=1, timeout=10,
                       action='http://127.0.0.1:5000/phonemenu/?node=end&again_dest=%s&last_dest=%s'%(again_dest, last_dest))
    g.addPlay( get_ggtts_url("重复收听，请按 * 键") )
    if with_again:
        g.addPlay( get_ggtts_url("返回上一层，请按 9") )
    g.addPlay( get_ggtts_url("结束请挂机") )


@route('/phonemenu/', method=['GET', 'POST'])
def phonemenu():
    u'''
    公司主菜单url
    '''
    # Default destination
    destination = 'default'
    # Get destination from url query string:
    # 'node' : destination
    # 'Digits' : input digits from user
    
    again_dest = request.args.get('again_dest', None)
    last_dest = request.args.get('last_dest', None)
    print '>>>>>>>>>>>',again_dest,last_dest
    
    if request.method == 'POST':
        node = request.args.get('node', None)
        dtmf = request.form.get('Digits', -1)
    else:
        node = request.args.get('node', None)
        dtmf = request.args.get('Digits', -1)
    if not node:
        node = 'default'
        
    if dtmf=='9':
        destination = "last"
    elif dtmf=='*':
        destination = "again"
    else:
        try:
            digits = int(dtmf)
        except ValueError:
            digits = -1
    
        if digits >= 0:
            try:
                destination = web[node][digits]
            except (KeyError, IndexError):
                destination = 'default'
        else:
            destination = node

    print "Destination %s" % str(destination)
    print "Digits %s" % str(dtmf)

    r = plivohelper.Response()
    #商业服务
    if destination == 'hours':
        r.addPlay( get_ggtts_url("平时，早上九点到下午五点") )
        r.addPlay( get_ggtts_url("周末，早上十点到下午三点") )
    #二级菜单
    elif destination == 'location':
        g = r.addGetDigits(numDigits=1, retries=3, timeout=10,
                   action='http://127.0.0.1:5000/phonemenu/?node=location')
        g.addPlay( get_ggtts_url("请选择水果") )
        g.addPlay( get_ggtts_url("西瓜，请按 1") )
        g.addPlay( get_ggtts_url("苹果，请按 2") )
        do_end(r,again_dest=destination, last_dest="default")
    elif destination == 'east-bay':
        r.addPlay( get_ggtts_url("西瓜堪称“瓜中之王”，原产于非洲。引入新疆是在唐代，五代时期引入中土") )
        r.addPlay( get_ggtts_url("西瓜中含有大量的水分，是一种可以滋身补体的食物和饮料") )
        do_end(r,again_dest=destination, last_dest="location")
    elif destination == 'san-jose':
        r.addPlay( get_ggtts_url("苹果，植物类水果，多次花果，具有丰富营养成分，有食疗、辅助治疗功能。") )
        do_end(r,again_dest=destination, last_dest="location")
    elif destination == 'duck':
        r.addPlay("http://yinyueshiting.baidu.com/data2/music/121524984/12152327672000128.mp3?xcode=73e5bdc48a52628b8bdc37595b2538486f8d94595cf48717")

    elif destination == 'receptionist':
        r.addPlay( get_ggtts_url("正在转接中，请稍等。"))
        g = r.addDial()
        g.addNumber("1002", gateways="user/,user/")
    elif destination == 'again':
        re = r.addRedirect("http://127.0.0.1:5000/phonemenu/?node=%s"%again_dest)
    elif destination == 'last':
        re = r.addRedirect("http://127.0.0.1:5000/phonemenu/?node=%s"%last_dest)
    else:
        # default menu
        g = r.addGetDigits(numDigits=1, timeout=10,
                           action='http://127.0.0.1:5000/phonemenu/?node=default')
        g.addPlay( get_ggtts_url("您好，欢迎来到捷优科技语音菜单测试") )
        g.addPlay( get_ggtts_url("了解服务时间, 请按 1") )
        g.addPlay( get_ggtts_url("二级菜单测试, 请按 2") )
        g.addPlay( get_ggtts_url("听首音乐, 请按 3") )
        g.addPlay( get_ggtts_url("转接人工服务, 请按 0") )
        
        do_end(r,again_dest=destination, last_dest=destination,with_again =False)


    print "RESTXML Response => %s" % r
    return jinja2_template('response_template.xml', response=r)

