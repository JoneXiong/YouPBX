# coding=utf-8

import os
import logging
import cPickle

from django.db import models

from apps.utils import sound_type_field

URL_PREFIX = '/oe_pbx/media'
_logger = logging.getLogger(__name__)

class MediaFile(models.Model):
    # parent = models.ForeignKey('self', verbose_name='父目录', blank=True, null=True, related_name="childs")
    # is_folder = models.BooleanField('文件夹', default=False)
    # name = models.CharField(u'名称', max_length=64, blank=True, null=True)
    tag = models.CharField(u'分类名', max_length=64, blank=True, null=True)
    comment = models.TextField(u'描述', blank=True,null=True)
    file_size = models.IntegerField('文件大小', default=0)
    true_path = models.CharField('物理路径',max_length=512)

    class Meta:
        app_label = 'base'
        verbose_name = u'语音库'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.true_path

    def path(self):
        return self.true_path

    @classmethod
    def get_path_from_id(cls,mid):
        obj = cls.objects.get(id=mid)
        return obj.true_path

    @staticmethod
    def sync(path = '/usr/local/freeswitch/sounds/'):
        for item in os.listdir(path):
            subpath = os.path.join(path, item);
            if os.path.isfile(subpath):
                _path = subpath.replace('/usr/local/freeswitch/sounds/','')
                _path_list = _path.rsplit('/',1)
                obj = MediaFile()
                if len(_path_list)>1:
                    obj.tag = _path_list[0]
                    obj.comment = _path_list[1]
                else:
                    obj.comment = _path
                obj.file_size = os.path.getsize(subpath)
                obj.true_path = _path
                obj.save()
            else:
               MediaFile.sync(subpath)


class PhraseMacro(models.Model):

    desc = models.CharField('说明',max_length=64)
    pause = models.IntegerField('停顿间隔',default=100)

    class Meta:
        app_label = 'base'
        verbose_name = u'语音包'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.desc

class PhraseItem(models.Model):

    phrase = models.ForeignKey(PhraseMacro,verbose_name="所属语音包",related_name="items")
    order = models.IntegerField('排序',blank=True, null=True)
    sound_type = sound_type_field()
    sound_content = models.CharField(u"内容", max_length=512, blank=True, null=True)

    class Meta:
        app_label = 'base'
        verbose_name = u'语音包项目'
        verbose_name_plural = verbose_name
