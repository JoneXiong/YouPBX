# coding=utf-8

from django.db import models


class Conference(models.Model):
    
    name = models.CharField(u'名称', max_length=64)
    pin = models.CharField(u'PIN', max_length=64)
    registry_record = models.BooleanField(u'Record conference?')
    registry_moh_type = models.CharField(u'Pre-Conference Music', max_length=50, choices=[('local_stream://moh',u'Music On Hold'), ('silence',u'Silence')], default='local_stream://moh')
    registry_energy_level = models.IntegerField(u'Minimum Energy Level' , default=20)
    registry_comfort_noise = models.BooleanField(u'Generate Comfort Noise?', default=True)
    number = models.ForeignKey('base.Number', verbose_name=u"选择号码")
    
    class Meta:
        app_label = 'funcs'
        verbose_name = u'语音会议室'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.name
