# coding=utf-8

import os
import logging
import cPickle

from django.db import models

URL_PREFIX = '/oe_pbx/media'
_logger = logging.getLogger(__name__)

class MediaFile(models.Model):
    parent = models.ForeignKey('self', verbose_name='父目录', blank=True, null=True, related_name="childs")
    is_folder = models.BooleanField('文件夹', default=False)
    name = models.CharField(u'名称', max_length=64, blank=True, null=True)
    comment = models.TextField(u'描述', blank=True,null=True)
    file_size = models.IntegerField('文件大小', default=0)
    ture_path = models.CharField('物理路径',max_length=512)
    
    class Meta:
        app_label = 'base'
        verbose_name = u'多媒体文件'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.ture_path
    

    def _get_path(self, cr, uid, ids, field_name, arg, context):
        result = {}
        
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.parent_id:
                path = '/'.join((obj.parent_id.path, obj.name or ''))
            else:
                path = obj.name
            result[obj.id] = path
        return result

    def _get_url(self, cr, uid, ids, field_name, arg, context):
        result = {}
        
        for obj in self.browse(cr, uid, ids, context=context):            
            result[obj.id] = '/'.join((URL_PREFIX, obj.path))
        return result

    def get_data(self, cr, uid, path, context=None):
        ids = self.search(cr, uid, [('path','=',path)], limit=1,context=context)
        if not ids:
            return ''
        return self.read(cr, uid, ids[0], ['data']).get('data') or ''
    
    def _data_get(self, cr, uid, ids, name, arg, context=None):
        if context is None:
            context = {}
        result = {}
        
        m_value = self.pool.get('ir.config_parameter').get_param(cr, uid, 'fs_sounds_path')
        if m_value:
            location = cPickle.loads(str(m_value))
        else:
            location = './oe_pbx_media'
        
        bin_size = context.get('bin_size')
        for attach in self.browse(cr, uid, ids, context=context):
            obj = attach
            if obj.parent_id:
                path = '/'.join((obj.parent_id.path, obj.name or ''))
            else:
                path = obj.name
            full_path = os.path.join(location, path)
            result[attach.id] = attach.db_datas#open(full_path,'rb').read().encode('base64')
        return result

    def _data_set(self, cr, uid, id, name, value, arg, context=None):
        if context is None:
            context = {}
            
        m_value = self.pool.get('ir.config_parameter').get_param(cr, uid, 'fs_sounds_path')
        if m_value:
            location = cPickle.loads(str(m_value))
        else:
            location = './oe_pbx_media'
            
        file_size = 0
        if location:
            obj = self.browse(cr, uid, id, context=context)
            if obj.parent_id:
                path = '/'.join((obj.parent_id.path, obj.name or ''))
            else:
                path = obj.name
            full_path = os.path.join(location, path)
            # delete file
            if full_path:
                if os.path.exists(full_path):
                    try:
                        if obj.is_folder:
                            os.unlink(full_path)
                    except OSError:
                        _logger.error("_file_delete could not unlink %s",full_path)
                    except IOError:
                        _logger.error("_file_delete could not unlink %s",full_path)
            # write file
            try:
                dirname = os.path.dirname(full_path)
                if not os.path.isdir(dirname):
                    os.makedirs(dirname)
                if obj.is_folder:
                    if not os.path.isdir(full_path):
                        os.makedirs(full_path)
                else:
                    bin_value = value.decode('base64')
                    file_size = len(bin_value)
                    open(full_path,'wb').write(bin_value)
            except IOError:
                _logger.error("_file_write writing %s",full_path)
            super(MediaFile, self).write(cr, uid, [id], {'db_datas': value, 'file_size': file_size, 'ture_path': full_path}, context=context)
        else:
            super(MediaFile, self).write(cr, uid, [id], {'db_datas': value, 'file_size': file_size, 'ture_path': full_path}, context=context)
        return True
    
    def unlink(self, cr, uid, ids, context=None):
        m_value = self.pool.get('ir.config_parameter').get_param(cr, uid, 'fs_sounds_path')
        if m_value:
            location = cPickle.loads(str(m_value))
        else:
            location = './oe_pbx_media'
        if location:
            for attach in self.browse(cr, uid, ids, context=context):
                if attach.path:
                    full_path = os.path.join(location, attach.path)
                    if os.path.exists(full_path):
                        try:
                            if attach.is_folder:
                                os.unlink(full_path)
                        except OSError:
                            _logger.error("_file_delete could not unlink %s",full_path)
                        except IOError:
                            _logger.error("_file_delete could not unlink %s",full_path)
        return super(MediaFile, self).unlink(cr, uid, ids, context)

