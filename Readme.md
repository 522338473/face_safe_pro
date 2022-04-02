# CSIA智能视图平台

CSIA智能视图平台 | 使用python3基于Django框架进行前后端不分离方式开发，以pipenv作为包管理工具
> 采用前后端不分离方式开发。前端扩展页面建议采用element-ui开发

## 安装

### 本地安装

1. 安装pip3，python3
   ```bash
   建议安装3.6.9系列Python工具包
   ```

2. 安装pipenv
   ```bash
   pip3 install pipenv -i https://pypi.tuna.tsinghua.edu.cn/simple/
   ```

3. 进入项目根目录
   ```bash
   cd face_safe_pro
   ```

4. 安装项目依赖
   ```bash
   pipenv sync && pipenv install --dev
   ```

## 运行

### 开发环境运行

1. 进入项目根目录
   ```bash
   cd face_safe_pro
   ```

2. 运行代码
   ```bash
   pipenv run python manage.py runserver 0.0.0.0:7878
   ```

3. 浏览器访问
   ```bash
   本地访问: http://127.0.0.1:7878/admin
   局域网访问: http://localip:7878/admin
   ```

4. 默认超级管理员账户账户
   ```bash
   用户名: admin
   密码: Admin!2345
   ```

---

## 目录结构

```
.
├── Dockerfile
├── Pipfile
├── Pipfile.lock
├── Readme.md
├── apps
│   ├── __init__.py
│   ├── account
│   │   ├── __init__.py
│   │   ├── admin.py   
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── archives
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── device
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── monitor
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── public
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── resources.py
│   │   ├── serializers.py
│   │   ├── templatetags
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── utils
│       ├── __init__.py
│       ├── constant.py
│       └── hasher.py
├── db.sqlite3
├── deployment
│   ├── __init__.py
│   └── record.py
├── docker-compose.yaml
├── face_safe_pro
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt  # 代码运行依赖
├── static
│   ├── favicon.ico  # 标签页logo
│   └── media  # 图片上传目录
│       ├── 1aRYX0FE.jpeg
└── templates
    ├── 404  # 404界面配置
    │   ├── 404.html
    │   └── 404.png
    └── admin  # 扩展页面配置根目录
        ├── archives
        │   ├── accessdiscover
        │   ├── archivesgroup
        │   ├── other
        │   │   ├── archives_count.html
        │   │   ├── archives_personnel.html
        │   │   └── search_person.html  # 人员档案-以人搜图页面配置
        │   └── personnel
        ├── change_list.html  # 默认列表页配置
        ├── device
        │   ├── deviceinfo
        │   │   ├── change_list.html  # 设备列表页自定义配置
        │   │   └── results
        │   │       ├── pagination.html  # 分页组件
        │   │       ├── table.html  # 数据页
        │   │       └── toolbar.html
        │   ├── deviceoffline
        │   ├── devicephoto
        │   ├── motor
        │   ├── other
        │   │   ├── alarm_list.html
        │   │   ├── real_time.html  # 实时监控页面
        │   │   ├── search_image.html  # 以图搜图页面
        │   │   ├── search_results.html
        │   │   ├── search_time.html  # 以时间搜图页面
        │   │   ├── snap_count.html
        │   │   └── video_snap.html
        │   └── vehicle
        ├── home.html  # 主页
        ├── home_page.html  # 主页扩展界面
        ├── index.html  # 首页
        ├── monitor
        │   ├── archiveslibrary
        │   ├── archivespersonnel
        │   ├── areamonitorpersonnel
        │   ├── areasnaprecord
        │   ├── monitor
        │   ├── monitordiscover
        │   ├── personneltype
        │   ├── photocluster
        │   ├── restrictedarea
        │   ├── vehiclemonitor
        │   └── vehiclemonitordiscover
        ├── parts
        │   ├── header.html
        │   └── quick.html
        └── timeline.html
```

> 默认列表页为: templates/admin/change_list.html 设备管理列表页: templates/admin/device/deviceinfo/change_list.html
>
> 如不配置用默认。如果配置用自己的

```
模板语法: 
{% alarm_list current_page=1 page_size=10 as alarm_list %}
{% for alarm in alarm_list.alarm_list %}
    <div>{{ alarm }}</div>
    <img src="{{ alarm.target__photo }}" alt="" width="10%">
    <img src="{{ alarm.record__head_path }}" alt="" width="10%">
    <a href="javascript:alert({{ alarm.target__name }})">查看详情</a>
    
    {% if page_name == 'search_image' %}
      <a href="javascript:alert('详情页面')">查看详情</a>
      {#     展示普通信息搜图结果       #}
    {% elif page_name == 'search_time' %}
         <a href="javascript:alert('详情页面')">查看详情</a>
         <a href="javascript:alert('轨迹页面')">轨迹搜索</a>
    {% else %}
   
    {% endif %}
{% endfor %}

{{ 变量 }}
{% 表达式 %}
{% include '模板继承' %}
{% block monitor %}
   ... 块继承
{% endblock %}  
```
