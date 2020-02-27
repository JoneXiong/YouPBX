# coding=utf-8

def sound_type_field():
    from django.db import models
    _choices = [
        ('audio',u'音频文件'),
        ('tts',u'TTS文字'),
        ('number',u'数字播报'),
        ('count',u'数目播报'),
        ('tts_var',u'TTS文字(变量)'),
        ('number_var',u'数字播报(变量)'),
        ('count_var',u'数目播报(变量)'),
    ]
    field = models.CharField(u'类型', max_length=20, choices=_choices, default='audio', blank=True, null=True)
    return field


def make_audio_selections(self):
    from xadmin import widgets
    from apps.extend.models import MediaFile
    return {
        'audio': widgets.ForeignKeyPopupWidget(self, MediaFile,'id'),
        'tts': widgets.AdminTextInputWidget(),
        'number': widgets.AdminTextInputWidget(),
        'count': widgets.AdminTextInputWidget(),
        'tts_var': widgets.AdminTextInputWidget(),
        'number_var': widgets.AdminTextInputWidget(),
        'count_var': widgets.AdminTextInputWidget(),
    }


action_type_choices = [
    ('device', u'分机'),
    ('ivr', u'IVR语音菜单'),
    ('conference', u'语音会议室'),
    #('queue', u'队列'),
    ('ringgroup', u'来电队列'),
    ('voicemail', u'语音邮箱'),
]

def make_action_to_selections(self):
    from xadmin import widgets
    from apps.funcs import models as funcs_models
    from apps.extend import models as extend_models
    return {
        'device':widgets.ForeignKeyPopupWidget(self, funcs_models.Device,'id'),
        'ivr': widgets.ForeignKeyPopupWidget(self, extend_models.IVR,'id'),
        'conference': widgets.ForeignKeyPopupWidget(self, funcs_models.Conference,'id'),
        #'queue': widgets.ForeignKeyPopupWidget(self,models.Queue,'id'),
        'ringgroup': widgets.ForeignKeyPopupWidget(self, funcs_models.RingGroup,'id'),
        'voicemail': widgets.ForeignKeyPopupWidget(self, funcs_models.VoiceMail,'id'),
    }

