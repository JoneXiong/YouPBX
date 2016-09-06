# -*- coding: utf-8 -*-

import os
import time
import random
import hashlib

import urlparse
import tempfile
import mimetypes

from django.conf import settings
from django.db import models
from django.core.exceptions import ImproperlyConfigured

import qiniu.rs
import qiniu.io
import qiniu.conf


for attr in ('QINIU_ACCESS_KEY', 'QINIU_SECRET_KEY', 'QINIU_BUCKET_DEFAULT'):
    if not hasattr(settings, attr):
        raise ImproperlyConfigured("You must define the %s before using django-qiniu" % attr)
qiniu.conf.ACCESS_KEY = settings.QINIU_ACCESS_KEY
qiniu.conf.SECRET_KEY = settings.QINIU_SECRET_KEY

def get_random_filename(basename=None, ext=None):
    name = hashlib.sha1(
            str(random.random()) + \
            str(time.time())).hexdigest()
    if basename:
        ext = os.path.splitext(basename)[1]
    if ext:
        name = '%s%s' % (name, ext)
    return name

def get_size(file):
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    return size

mimetypes.init()

TEMP_FILE_SIZE = 1024 * 1024


class QiNiuFileDescriptor(object):
    """
    Descriptor for qiniu
    """
    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))

        file = instance.__dict__[self.field.name]
        if file is None:
            return None
        elif isinstance(file, basestring):
            # Old qiniu file
            attr = self.field.attr_class(instance, self.field, file)
            if os.path.exists(file):
                attr.file = file
            else:
                attr = self.field.attr_class(instance, self.field, file, key=file)
            instance.__dict__[self.field.name] = attr
        elif isinstance(file, self.field.attr_class):
            return file 
        else:
            # file-like object
            file_copy = self.field.attr_class(instance, self.field, file.name)
            file.seek(0, 0)
            file_copy.file = file
            instance.__dict__[self.field.name] = file_copy

        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value


class QiNiuFileAttrClass(object):
    file = None

    def __init__(self, instance, field, name, key=None):
        self.instance = instance
        self.field = field
        self.name = name
        self.key = key

    @property
    def url(self):
        if not self.key:
            raise AttributeError('Can not get url of unsaved field.')
        return urlparse.urljoin('http://%s' % self.field.domain, self.key)

class QiNiuImageAttrClass(QiNiuFileAttrClass):

    def get_image_display(self, display):
        return '%s-%s' % (self.url, display)

    def get_image_view(self, mode=1, width=None, height=None, quality=None, format=None):
        target = []
        target.append('%s' % mode)
        
        if width is not None:
            target.append("w/%s" % width)
        if height is not None:
            target.append("h/%s" % height)
        if quality is not None:
            target.append("q/%s" % quality)
        if format is not None:
            target.append("format/%s" % format)
        return "%s?imageView/%s" % (self.url, '/'.join(target))


class QiNiuFileField(models.TextField):

    attr_class = QiNiuFileAttrClass
    descriptor_class = QiNiuFileDescriptor
    description = 'File field for qiniu storage'

    def __init__(self, *args, **kwargs):
        self.upload_bucket = kwargs.pop('upload_buckent', settings.QINIU_BUCKET_DEFAULT)
        self.upload_to = kwargs.pop('upload_to', None)
        self.domain = kwargs.pop('domain', '%s.qiniudn.com' % self.upload_bucket)
        super(QiNiuFileField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def contribute_to_class(self, cls, name):
        super(QiNiuFileField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, self.descriptor_class(self))

    def get_uptoken(self):
        policy = qiniu.rs.PutPolicy(self.upload_bucket)
        return policy.token()

    def pre_save(self, model_instance, add):
        """
        Upload file to qiniu server

        Args:
        ~~~~~

        - value, String or File-like object

        """
        value = getattr(model_instance, self.attname)
        if not value:
            return value
        if not value.file:
            return value.key
        if not self.upload_to:
            raise Exception('Must specify upload_to')

        filename = value.name
        key = self.upload_to(instance=model_instance, filename=filename)

        if isinstance(value.file, basestring):
            ret, err = qiniu.io.put_file(self.get_uptoken(), key, value.file)
        # If file is too large, we should generate a tempfile
        if get_size(value.file) > TEMP_FILE_SIZE:
            ext = os.path.splitext(filename)[1]
            filename_temp = tempfile.mkstemp(ext)[1]
            with open(filename_temp, 'wb') as fp:
                fp.write(value.file.read())

            # Upload File
            ret, err = qiniu.io.put_file(self.get_uptoken(), key, filename_temp)
            try:
                os.remove(filename_temp)
            except:
                pass
        else:
            # Upload binary stream
            extra = qiniu.io.PutExtra()
            extra.mime_type = mimetypes.guess_type(filename)[0] or 'text/plain'

            ret, err = qiniu.io.put(self.get_uptoken(), key, value.file, extra)

        if err is not None:
            raise Exception(err)


        value.file.seek(0, 0)
        value.key = key
        setattr(model_instance, self.attname, key)
        return key


class QiNiuImageField(QiNiuFileField):
    attr_class = QiNiuImageAttrClass

# Fix south problems
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^xadmin\.qiniu_fields\.QiNiuFileField"])
    add_introspection_rules([], ["^xadmin\.qiniu_fields\.QiNiuImageField"])
except ImportError:
    pass

