## diancan_server

1、项目搭建

```
pip install django==2.1.7 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install djangorestframework==3.9.3
pip install Pillow==6.0.0
pip install djangorestframework-jwt==1.11.0
django-cors-headers==2.5.3
django-filter==2.1.0
```

2、启动django项目

```
python manage.py runserver 127.0.0.1:9000

如果出现一下报错信息请更换端口重试
System check identified no issues (0 silenced).
December 24, 2019 - 15:21:57
Django version 2.1.7, using settings 'diancan_server.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
Error: [WinError 10013] 以一种访问权限不允许的方式做了一个访问套接字的尝试。

```

3、调整目录

```
├── docs/          # 项目相关资料保存目录
├── logs/          # 项目运行时/开发时日志目录
├── manage.py
├── diancan_server/         # 项目主应用，开发时的代码保存
│   ├── apps/      # 开发者的代码保存目录，以模块[子应用]为目录保存
│   ├── libs/      # 第三方类库的保存目录[第三方组件、模块]
│   ├── settings/
│       ├── dev.py   # 项目开发时的本地配置
│       ├── prop.py  # 项目上线时的运行配置
│   ├── urls.py    # 总路由
│   ├── utils/     # 多个模块[子应用]的公共函数类库[自己开发的组件]
└── scripts/       # 保存项目运营时的脚本文件
```

3.1更改manage.py和wsgi.py文件中的配置

```
manage.py

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diancan_server.settings.dev')
    
```

```
diancan_server/wsgi.py

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diancan_server.settings.dev')

application = get_wsgi_application()
```

如果是在pycharm中运行还需要在运行配置中修改配置路径

#### 4 Xadmin

xadmin是Django的第三方扩展，比使用Django的admin站点更强大也更方便。

文档：https://xadmin.readthedocs.io/en/latest/index.html

#### 4.1. 安装

通过如下命令安装xadmin的最新版

```shell
pip install https://codeload.github.com/sshwsfc/xadmin/zip/django2
```

在配置文件中注册如下应用

```python
INSTALLED_APPS = [
    ...
    'xadmin',
    'crispy_forms',
    'reversion',
    ...
]

# 修改使用中文界面
LANGUAGE_CODE = 'zh-Hans'

# 修改时区
TIME_ZONE = 'Asia/Shanghai'
```



xadmin有建立自己的数据库模型类，需要进行数据库迁移

```shell
python manage.py makemigrations
python manage.py migrate
```



在总路由中添加xadmin的路由信息

```python
import xadmin
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    path(r'xadmin/', xadmin.site.urls),
]
```



如果之前没有创建超级用户，需要创建，如果有了，则可以直接使用之前的。

```python
python manage.py createsuperuser

用户名 root
密码 123

```

在浏览器输入以下路由可访问xadmin后台管理

```
http://127.0.0.1:9000/xadmin/
```



5、创建home子应用

```
切换到apps目录
python manage.py startapp
```

6、安装redis
```
https://www.jianshu.com/p/e16d23e358c0
https://github.com/MicrosoftArchive/redis/releases
https://blog.csdn.net/ZZY1078689276/article/details/79429227
```
切换到redis安装目录
```
redis-server.exe redis.windows.conf
redis-cli.exe -h 127.0.0.1 -p 6379

```


