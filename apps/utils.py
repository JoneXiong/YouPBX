# coding=utf-8

def sound_type_field():
    from django.db import models
    field = models.CharField(u'类型', max_length=20, choices=[
                                                              ('audio',u'音频文件'),
                                                              ('tts',u'TTS文字'),
                                                              ('number',u'数字播报'),
                                                              ('count',u'数目播报'),
                                                              ('tts_var',u'TTS文字(变量)'),
                                                              ('number_var',u'数字播报(变量)'),
                                                              ('count_var',u'数目播报(变量)'),
                                                              ], default='audio', blank=True, null=True)
    return field
