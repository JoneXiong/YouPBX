# coding=utf-8

from django.db import models

class NumberPool(models.Model):
    
    name = models.CharField(u'名称', max_length=64)
    alias = models.CharField(u'别名', max_length=64, null=True, blank=True)
    count = models.IntegerField(u'号码数量', null=True, blank=True)
    no = models.CharField(u'编号', max_length=64, null=True, blank=True)
    
    class Meta:
        app_label = 'base'
        verbose_name = u'号码池'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.name
    
class Number(models.Model):
    
    number = models.CharField(u'号码', max_length=64)
    location = models.ForeignKey('base.Location', verbose_name="位置/域", default=1)
    context = models.ForeignKey('base.Context', verbose_name="所属组(context)", default=1)
    numberpool = models.ForeignKey(NumberPool, verbose_name="所属号码池", default=1)
    used = models.BooleanField('是否已被使用', default=False)
    terminate_action = models.CharField(u'无应答处理模式', max_length=20, choices=[
                                                                            ('hangup',u'直接挂断'),
                                                                            ('voicemail',u'发送语音邮件'),
                                                                            ('transfer',u'转接到')
                                                                            ], default='hangup')
    transfer_type = models.CharField(u'转接类型', max_length=20, choices=[
                        ('device', u'Device (分机)'),
                        ('autoattendant', u'Auto Attendant (自动语音应答)'),
                        ('conference', u'Conference (语音会议室)'),
                        #('5', u'External Xfer'),
                        ('ringgroup', u'Ring Group (来电队列)'),
                        ('voicemail', u'Voicemail (语音邮箱)'),
                        ('timeroutes', u'TimeRoutes (工作时段)')
                                                                            ], null=True, blank=True)
    transfer_to_id = models.IntegerField(u'转接对象', null=True, blank=True)
    
    vm = models.IntegerField('语音邮箱', null=True, blank=True)
    
    class Meta:
        app_label = 'base'
        verbose_name = u'号码'
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.number
    
    def _action(self, cursor, user, ids, name, arg, context=None):
        res = {}
        ir_values_obj = self.pool.get('ir.values')
        value_ids = ir_values_obj.search(cursor, user, [
            ('model', '=', self._name), ('key', '=', 'action'),
            ('key2', '=', 'fs_transfer_open'), ('res_id', 'in', ids)],
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
            ('key2', '=', 'fs_transfer_open'), ('res_id', '=', menu_id)],
            context=context)
        if value and values_ids:
            ir_values_obj.write(cursor, user, values_ids, {'value': value}, context=ctx)
        elif value:
            # no values_ids, create binding
            ir_values_obj.create(cursor, user, {
                'name': u'fs_transfer',
                'model': self._name,
                'value': value,
                'key': 'action',
                'key2': 'fs_transfer_open',
                'res_id': menu_id,
                }, context=ctx)
        elif values_ids:
            # value is False, remove existing binding
            ir_values_obj.unlink(cursor, user, values_ids, context=ctx)

    def get_vm_number(self):
        pass
    
    def get_transfer_number(self):
        pass
