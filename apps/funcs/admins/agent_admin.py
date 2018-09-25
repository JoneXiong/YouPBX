# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon
from xadmin import widgets
from xadmin import layout
from xadmin.views import filter_hook

from apps.funcs import models
from apps.common import ReXmlAdmin


class AgentSkillInline(object):
    model = models.AgentSkill
    extra = 1
    style = 'table'

class AgentAdmin(object):
    app_label = 'funcs'
    menu_group = 'agentset_group'
    order = 7
    inlines = [AgentSkillInline]

    user_fields = ['uid']
    #user_can_access_owned_objects_only = True
    #user_owned_objects_field = 'uid'
    #remove_permissions = ['delete']
    search_fields = ['number']
    can_delete_multi = False

    form_layout = [
        layout.TabHolder(
            layout.Tab(
                '基本设置',
                'number','nickname','answer_way',
                'group',
                layout.Row('is_group_admin', 'is_corp_admin'),
                css_id = 'tab1'
            ),
            layout.Tab(
                '高级设置',
                'atype','simo','timeout',
                'busy_delay_time','reject_delay_time','max_no_answer',
                'call_power','can_out_call','can_in_record','can_out_record',
                css_id = 'tab2'
            )
        )
        ]

    def get_cur_agent(self):
        try:
            return self.user.profile.agent
        except:
            return None

    def do_add(self):
        from dao import agent_dao
        from apps.base.models import Number
        from django.contrib.auth.models import User

        obj = self.new_obj
        _number = obj.number
        # 号码限定为当前坐席的前缀
        cur_agent = self.get_cur_agent()
        if cur_agent:
            pre = str(cur_agent.number)[0]
            _min = '%s001'%pre
            _max = '%s999'%pre
            is_mid = int(_number)>=int(_min) and int(_number)<=int(_max)
            if len(str(_number))!=4 or str(_number)[0]!=pre or not is_mid:
                return u'号码必须为 %s - %s 范围内的4位数字'%(_min,_max)
        try:
            Number.objects.get(number=_number)
            return u'号码已经存在'
        except:
            try:
                User.objects.get(username=str(_number))
                return '该号码的用户已经存在'
            except:
                pass
            # 创建号码
            nb = Number()
            nb.number = _number
            nb.numberpool_id = 1
            nb.save()

            # 创建分机
            device = models.Device()
            device.number_id = nb.id
            device.name = _number
            device.sip_password = '654321'
            # 分机context默认为当前操作员坐席分机的context
            if cur_agent:
                device.context = cur_agent.device.context
            device.save()

            obj.device_id = device.id
            super(AgentAdmin,self).do_add()
            _perm = {}
            if obj.is_corp_admin:
                _perm['is_admin'] = True
            if obj.is_group_admin:
                _perm['is_grouper'] = True
            new_user = agent_dao.create_user(str(obj.number),'654321',obj.id, **_perm)
            # 当为超管时记录的创建人设为自己
            if not cur_agent:
                obj.uid = new_user.id
                obj.save()
            # 触发同步到fs
            from apps.common import ReXmlAdmin
            ReXmlAdmin()._rexml()

    def do_update(self):
        from dao import agent_dao
        self.org_obj = self.get_org()
        _perm = {}
        if self.org_obj.is_corp_admin!=self.new_obj.is_corp_admin:
            _perm['is_admin'] = self.new_obj.is_corp_admin
        if self.org_obj.is_group_admin!=self.new_obj.is_group_admin:
            _perm['is_grouper'] = self.new_obj.is_group_admin
        agent_dao.update_user(str(self.new_obj.number), **_perm)
        super(AgentAdmin,self).do_update()

    def do_delete(self):
        from dao import agent_dao
        if not self.user.is_superuser:
            if str(self.obj.number)[0]!=self.user.username[0]:
                return u'非法操作'
        self.obj.device.number.delete()
        self.obj.device.delete()
        agent_dao.delete_user(str(self.obj.number))
        super(AgentAdmin,self).do_delete()
        # 触发同步到fs
        from apps.common import ReXmlAdmin
        ReXmlAdmin()._rexml()

    @filter_hook
    def get_readonly_fields(self):
        if self.org_obj:
            return ['number']
        else:
            return []

    def get_field_attrs(self, db_field, **kwargs):
        from xadmin import widgets
        attrs = super(AgentAdmin, self).get_field_attrs(db_field, **kwargs)
        if db_field.name == 'group':
            attrs['widget'] = widgets.ForeignKeyPopupWidget(self, models.Group, 'id')
        return attrs

    def check_group_admin(self):
        user = self.user
        if user.username[1:]=='000':
            return True
        return user.groups.filter(id=1).count()>0

    def queryset(self):
        qs = super(AgentAdmin,self).queryset()
        if self.user.is_superuser:
            return qs
        if self.check_group_admin():
            pre = self.user.username[0]
            _min = '%s000'%pre
            _max = '%s999'%pre
            return qs.filter(number__gte=int(_min), number__lte=int(_max))
        return qs.filter(id=-1)

site.register(models.Agent, AgentAdmin)


class SkillAdmin(object):
    app_label = 'funcs'
    menu_group = 'agentset_group'
    order = 7
site.register(models.Skill, SkillAdmin)

#site.register(models.AgentSkill)


class GroupAdmin(object):
    app_label = 'funcs'
    menu_group = 'agentset_group'
    order = 7

    user_fields = ['uid']
    user_can_access_owned_objects_only = True
    user_owned_objects_field = 'uid'
site.register(models.Group, GroupAdmin)
