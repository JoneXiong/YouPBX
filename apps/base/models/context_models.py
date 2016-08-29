# coding=utf-8

from django.db import models

class Context(models.Model):
    
    name = models.CharField(u'名称', max_length=64)
    media_mode = models.CharField(u'音频传输模式', max_length=10, choices=[('psp',u'服务器中转'),('p2p',u'点对点')], default='psp')
    end_type = models.CharField(u'无路由提示类型', max_length=10, choices=[('audio',u'音频文件'),('tts',u'TTS文字')], default='tts')
    media_file = models.ForeignKey('base.MediaFile', verbose_name=u"文件", blank=True,null=True)
    tts_string = models.TextField(u'TTS文字内容', blank=True,null=True)
    
    class Meta:
        app_label = 'base'
        verbose_name = u'组 context'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.name
    