
originate = "originate user/1000 &playback(/usr/local/freeswitch/sounds/en/us/callie/base256/8000/liberty.wav)"

# callExtension
"originate {origination_caller_id_name=Click-To-Call,ringback=\'%(2000,4000,440.0,480.0)\'}user/1000@xxx_context &transfer('xxx_ext XML sbc10.vwna.com') "

# callOutbound
# "originate", "{ringback=\'%(2000,4000,440.0,480.0)\',origination_caller_id_name=Click-To-Call,effective_caller_id_number="+str(origination_caller_id_number)+"}user/"+str(user.portal_extension)+"@"+str(context)+" &bridge(sofia/gateway/"+str(user.get_gateway())+"/"+str(did)+")"

# name="db.conf" description="LIMIT DB Configuration"
# name="callcenter.conf" description="CallCenter"
# name="fifo.conf" description="FIFO Configuration"
# name="lcr.conf" description="LCR Configuration"
# name='sofia.conf' description='sofia endpoint'
# name="voicemail.conf" description="Voicemail"
# name="acl.conf" description="Network Lists"

# sip_registrations表  用户/分机注册状态