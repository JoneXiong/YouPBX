# coding=utf-8

from django.db import models

from apps.utils import sound_type_field

class Extension(models.Model):

    desc = models.CharField(u"名称描述", max_length=64, blank=True, null=True)
    sound_type = sound_type_field()
    sound_content = models.CharField(u"内容", max_length=512, blank=True, null=True)
    phrase = models.ForeignKey("base.PhraseMacro",verbose_name="语音包",related_name="extroutes", blank=True, null=True)
    action_type = models.CharField(u'跳转类型', max_length=20, choices=[
                        ('device', u'分机'),
                        ('ivr', u'IVR语音菜单'),
                        ('conference', u'语音会议室'),
                        #('queue', u'队列'),
                        ('voicemail', u'语音邮箱'),
                    ], default='queue')
    action_to_id = models.IntegerField(u'跳转到', null=True, blank=True)

    class Meta:
        app_label = 'funcs'
        verbose_name = u'语音导航'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '%s(%s)'%(self.get_action_type_display(),self.action_to_id)

    def get_app(self):
        if self.action_type=='device':
            return 'transfer', '%s  XML context_1'%self.action_to_id
        elif self.action_type=='ivr':
            return 'ivr', 'oe_ivr_%s'%self.action_to_id
        else:
            return '',''

    def get_playback(self):
        stype = self.sound_type
        content = self.sound_content
        if content:
            if stype=='audio':
                return content.replace('zh/cn/sue/','')
                from apps.base.models import MediaFile
                return MediaFile.get_path_from_id(content)
            elif stype=="tts":
                return "say:tts_commandline:xiaoyan:%s"%content
            elif stype=="number":
                return "say:zh:NUMBER:ITERATED:%s"%content
            elif stype=="count":
                return "say:zh:NUMBER:PRONOUNCED:%s"%content
            else:
                return ''
        else:
            return ''

class ExtensionRoute(models.Model):

    class Meta:
        app_label = 'funcs'
        verbose_name = u'呼入路由设置'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.id
