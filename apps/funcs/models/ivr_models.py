# coding=utf-8
'''
IVR相关模型
'''

from django.db import models

from  apps.utils import sound_type_field

def sound_field():
    field = models.CharField(u'类型', max_length=20, choices=[
                                                              ('audio',u'音频文件'),
                                                              ('tts',u'TTS文字'),
                                                              ('number',u'数字播报'),
                                                              ('count',u'数目播报'),
                                                              
                                                              ('tts_var',u'TTS文字(变量)'),
                                                              ('number_var',u'数字播报(变量)'),
                                                              ('count_var',u'数目播报(变量)'),
                                                              ], default='audio')
    return field

class IVR(models.Model):

    name = models.CharField(u'名称', max_length=64)

    greet_long_type = sound_type_field()
    greet_long_content = models.CharField(u"内容", max_length=512, blank=True, null=True)


    greet_short_type = sound_type_field()
    greet_short_content = models.CharField(u"内容", max_length=512, blank=True, null=True)

    invalid_sound_type = sound_type_field()
    invalid_sound_content = models.CharField(u"内容", max_length=512, blank=True, null=True)

    exit_sound_type = sound_type_field()
    exit_sound_content = models.CharField(u"内容", max_length=512, blank=True, null=True)

    registry_max_failures = models.IntegerField('最多尝试次数', default=3)
    digit_timeout = models.IntegerField('按键最大间隔时间', default=2)
    timeout = models.IntegerField('输入超时时间', default=10)
    max_timeouts = models.IntegerField('最大超时次数', default=3)
    extension_digits = models.IntegerField('最大收号位数', default=1)

    class Meta:
        app_label = 'funcs'
        verbose_name = u'IVR菜单'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def _get_sound(self, stype, content):
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

    def get_greet_long(self):
        return self._get_sound(self.greet_long_type, self.greet_long_content)

    def get_greet_short(self):
        return self._get_sound(self.greet_short_type, self.greet_short_content)

    def get_invalid_sound(self):
        return self._get_sound(self.invalid_sound_type, self.invalid_sound_content)

    def get_exit_sound(self):
        return self._get_sound(self.exit_sound_type, self.exit_sound_content)


class IVRKeymapping(models.Model):

    ivr = models.ForeignKey(IVR, verbose_name=u"所属语音应答", related_name = 'keymappings')
    digits = models.CharField(u'键', max_length=64)
    action_type = models.CharField(u'动作类型', max_length=20, choices=[
                        ('device', u'分机'),
                        ('ivr', u'IVR语音菜单'),
                        ('conference', u'语音会议室'),
                        ('queue', u'队列'),
                        ('voicemail', u'语音邮箱'),
                        
                        ('parent', u'返回上层')
                    ])
    action_to_id = models.IntegerField(u'动作对象', null=True, blank=True)

    class Meta:
        app_label = 'funcs'
        verbose_name = u'键映射'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.digits

    def get_number(self):
        from apps.base.models import Number
        return Number.objects.get(id=1)

    def get_exec(self):
        if self.action_type=='device':
            return 'menu-exec-app', 'transfer %s  XML context_1'%self.action_to_id
        elif self.action_type=='ivr':
            return 'menu-sub', 'oe_ivr_%s'%self.action_to_id
        elif self.action_type=='queue':
            return 'menu-exec-app', "execute_extension set:QueueID=%s,socket:'127.0.0.1:8085 async full' inline"%self.action_to_id

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

