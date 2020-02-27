# YouPBX
A great GUI manager for FreeSwitch

# 概述

YouPBX 是一个强大 FreeSwift (电话软交换系统) 的管理GUI系统，基于Django开发，功能全面，体验友好，可以基于此项目做一个完善的IPPBX系统、呼叫中心应用等

# 使用

1. git clone
2. cd YouPBX
3. 项目界面框架用的 [DjangoX](https://github.com/JoneXiong/DjangoX), 请拷贝xadmin包到运行根目录
4. cp config_sample.py config.py 编辑配置freeswitch的连接信息
4. 执行Django migrations命令 初始化数据库，执行Django createsuperuser创建管理员账号
5. python manage.py runserver 0.0.0.0:8080 运行服务
6. 浏览 http://localhost/


# 预览
![info](https://github.com/JoneXiong/YouPBX/raw/master/apps/base/static/base/images/youpbx0.jpg)

![info](https://github.com/JoneXiong/YouPBX/raw/master/apps/base/static/base/images/youpbx1.jpg)

![info](https://github.com/JoneXiong/YouPBX/raw/master/apps/base/static/base/images/youpbx2.jpg)

## 讨论
PBX应用开发交流群 34288838

## 获取商业支持
联系 QQ 669229467
