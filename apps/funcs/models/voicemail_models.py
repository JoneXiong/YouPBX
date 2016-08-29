# coding=utf-8

from django.db import models


class VoiceMail(models.Model):
    
    name = models.CharField(u'名称', max_length=64)
    mailbox = models.CharField(u'名称', max_length=64, blank=True, null=True)
    password = models.CharField(u'名称', max_length=64, blank=True, null=True)
    registry_email_all_messages = models.BooleanField(u'Email All Messages')
    registry_email_address = models.CharField(u'Email Address', max_length=128, blank=True, null=True)
    registry_delete_file = models.BooleanField(u'Delete Message After Emailing')
    registry_attach_audio_file = models.BooleanField(u'Attach Audio to Email')
    
    number = models.ForeignKey('base.Number', verbose_name="选择号码")
    skipInstructions = models.BooleanField(u'Skip Voicemail Instructions')
    skipGreeting = models.BooleanField(u'Skip Voicemail Greeting')
    
    class Meta:
        app_label = 'funcs'
        verbose_name = u'语音邮箱'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.name
    