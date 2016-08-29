# coding=utf-8

from django.db import models


class Autoattendant(models.Model):
    
    name = models.CharField(u'名称', max_length=64)
    registry_type = models.CharField(u'提示类型', max_length=20, choices=[('audio',u'音频文件'),('tts',u'TTS文字')], default='audio')
    registry_mediafile = models.ForeignKey('base.MediaFile', verbose_name=u"文件", blank=True, null=True)
    registry_tts_string = models.TextField(u"TTS文字内容", blank=True, null=True)
    registry_max_failures = models.IntegerField(u'最多尝试次数', default=3)
    digit_timeout = models.IntegerField(u'数字超时时间', default=2)
    timeout = models.IntegerField(u'输入超时时间', default=10)
    extension_context = models.ForeignKey('base.Context', verbose_name=u"扩展网络组", default=1)
    extension_digits = models.IntegerField(u'扩展长度', default=4)
    number = models.ForeignKey('base.Number', verbose_name=u"选择号码")
    
    class Meta:
        app_label = 'funcs'
        verbose_name = u'自动语音应答'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.name
    

class AutoattendantKeymapping(models.Model):
    
    autoattendant = models.ForeignKey(Autoattendant, verbose_name=u"所属语音应答", related_name = 'keymappings')
    digits = models.CharField(u'键', max_length=64)
    action_type = models.CharField(u'动作类型', max_length=20, choices=[
                        ('device', u'Device (分机)'),
                        ('autoattendant', u'Auto Attendant (自动语音应答)'),
                        ('conference', u'Conference (语音会议室)'),
                        #('5', u'External Xfer'),
                        ('ringgroup', u'Ring Group (来电队列)'),
                        ('voicemail', u'Voicemail (语音邮箱)'),
                        ('timeroutes', u'TimeRoutes (工作时段)')
                    ])
    action_to_id = models.IntegerField(u'动作对象', null=True, blank=True)
    
    class Meta:
        app_label = 'funcs'
        verbose_name = u'自动语音应答键映射'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.digits
    
    def _action(self, cursor, user, ids, name, arg, context=None):
        res = {}
        ir_values_obj = self.pool.get('ir.values')
        value_ids = ir_values_obj.search(cursor, user, [
            ('model', '=', self._name), ('key', '=', 'action'),
            ('key2', '=', 'fs_ivrkey_open'), ('res_id', 'in', ids)],
            context=context)
        values_action = {}
        for value in ir_values_obj.browse(cursor, user, value_ids, context=context):
            values_action[value.res_id] = value.value
        for menu_id in ids:
            res[menu_id] = values_action.get(menu_id, False)
        return res

    def _action_inv(self, cursor, user, menu_id, name, value, arg, context=None):
        if context is None:
            context = {}
        ctx = context.copy()
        if self.CONCURRENCY_CHECK_FIELD in ctx:
            del ctx[self.CONCURRENCY_CHECK_FIELD]
        ir_values_obj = self.pool.get('ir.values')
        values_ids = ir_values_obj.search(cursor, user, [
            ('model', '=', self._name), ('key', '=', 'action'),
            ('key2', '=', 'fs_ivrkey_open'), ('res_id', '=', menu_id)],
            context=context)
        if value and values_ids:
            # 修改
            ir_values_obj.write(cursor, user, values_ids, {'value': value}, context=ctx)
        elif value:
            # 新增
            # no values_ids, create binding
            ir_values_obj.create(cursor, user, {
                'name': u'fs_ivr_key_mapping',
                'model': self._name,
                'value': value,
                'key': 'action',
                'key2': 'fs_ivrkey_open',
                'res_id': menu_id,
                }, context=ctx)
        elif values_ids:
            # 删除
            # value is False, remove existing binding
            ir_values_obj.unlink(cursor, user, values_ids, context=ctx)
    
