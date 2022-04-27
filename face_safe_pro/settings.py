"""
Django settings for face_safe_pro project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import sys
import datetime
from pathlib import Path

from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 将apps目录加入系统环境变量
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# logs目录配置
LOG_PATH = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-e)(zf09nkj)s^8nt+2wpcibw^3f)55l-hg4fc6mr4yt%@w-ox'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DJANGO_DEBUG', 1)))

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simplepro',
    'simpleui',
    'import_export',
    'corsheaders',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_celery_beat',

    'apps.public',
    'apps.account',
    'apps.device',
    'apps.archives',
    'apps.monitor'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simplepro.middlewares.SimpleMiddleware',
]

ROOT_URLCONF = 'face_safe_pro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'face_safe_pro.wsgi.application'
ASGI_APPLICATION = 'face_safe_pro.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'pg': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'face_safe_pro_test'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', '192.168.3.19'),
        'PORT': int(os.getenv('DB_PORT', 5432)),
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASES['default'] = DATABASES[os.getenv('DJANGO_DATABASE', 'sqlite')]

# django3.2之前主键默认int类型，3.2之后默认bigint
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# 全局时间格式化
# DATETIME_FORMAT = "Y-m-d H:i:sO"
# date_format = 'Y-m-d'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


# 静态文件配置
STATIC_URL = '/static/'

# 生产环境目录
STATIC_ROOT = BASE_DIR / 'static'

# 开发阶段
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles')
]

# 图片上传配置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

REDIS_SITE = ("redis://{}:{}/{}".format(
    os.getenv('REDIS_SERVER_HOST', '192.168.2.95'),
    os.getenv('REDIS_SERVER_PORT', '6379'),
    os.getenv('REDIS_CACHE_DB', '1'))
)
REDIS_SERVER_HOST = os.getenv('REDIS_SERVER_HOST', '192.168.2.95')
REDIS_SERVER_PORT = os.getenv('REDIS_SERVER_PORT', 6379)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_SITE,
        "TIMEOUT": 60 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}  # 连接池
        }
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s - %(levelname)s - %(lineno)03d] %(message)s'
        }
    },
    'filters': {

    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'server.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'error.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'redis': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'redis.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'celery': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'celery.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        }
    },
    'loggers': {
        'server.default': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False,
        },
        'server.error': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': False,
        },
        'server.redis': {
            'handlers': ['redis'],
            'level': 'INFO',
            'propagate': False,
        },
        'server.celery': {
            'handlers': ['celery'],
            'level': 'INFO',
            'propagate': False,
        },
        # # SQL输出调试
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'propagate': True,
        #     'level': 'DEBUG',
        # },
    }
}

# 文件存储FastDFS_CONFIG
FAST_DFS_HOST = os.getenv('FAST_DFS_HOST', 'http://192.168.2.95')

# 隐藏右侧SimpleUI广告链接和使用分析
SIMPLEUI_HOME_INFO = True
SIMPLEUI_ANALYSIS = True

# 默认读取本地资源
SIMPLEUI_STATIC_OFFLINE = True

# 首页配置
# SIMPLEUI_HOME_TITLE = '自定义首页'
# SIMPLEUI_HOME_PAGE = 'https://www.baidu.com'
# SIMPLEUI_HOME_ICON = 'fa fa-user'
SIMPLEPRO_MONIT_DISPLAY = True
SIMPLEPRO_INFO = False

# 配置Simple Pro是否显示首页的图标，默认为True，显示图表，False不显示
SIMPLEPRO_CHART_DISPLAY = True

# SIMPLEUI_LOGO='https://mat1.gtimg.com/pingjs/ext2020/qqindex2018/dist/img/qq_logo_2x.png'


# 首页快速操作
SIMPLEUI_HOME_QUICK = True

# # 设置simpleui 点击首页图标跳转的地址
# SIMPLEUI_INDEX = 'https://www.88cto.com'

# 菜单配置后期置换
SIMPLEUI_CONFIG = {
    'system_keep': False,
    'dynamic': False,
    'menus': [
        {
            'name': '实时监控',
            'icon': 'fa fa-desktop',
            'url': '/v1/device/real_time/'
        },
        {
            'name': '抓拍记录',
            'icon': 'fab fa-snapchat',
            'url': '/admin/device/devicephoto/'
        },
        {
            'name': '重点人员',
            'icon': 'fa fa-user-tie',
            'models': [
                {
                    'name': '重点人员分类',
                    'icon': 'fa fa-user-tie',
                    'url': '/admin/monitor/personneltype/'
                },
                {
                    'name': '重点人员',
                    'icon': 'fa fa-user-tie',
                    'url': '/admin/monitor/monitor/'
                },
                {
                    'name': '报警信息',
                    'icon': 'fas fa-comment',
                    'url': '/admin/monitor/monitordiscover/'
                }
            ]
        },
        {
            'name': '关注人员',
            'icon': 'fa fa-user-astronaut',
            'models': [
                {
                    'name': '人像库',
                    'icon': 'fa fa-user-astronaut',
                    'url': '/admin/monitor/archiveslibrary/'
                },
                {
                    'name': '关注人员',
                    'icon': 'fa fa-user-astronaut',
                    'url': '/admin/monitor/archivespersonnel/'
                },
                {
                    'name': '轨迹档案',
                    'icon': 'fa fa-user-astronaut',
                    'url': '/admin/monitor/photocluster/'
                }
            ],
        },
        {
            'name': '人员档案',
            'icon': 'fa fa-box',
            'models': [
                {
                    'name': '档案库',
                    'icon': 'fa fa-box',
                    'url': '/admin/archives/archivesgroup/'
                },
                {
                    'name': '档案人员',
                    'icon': 'fa fa-id-card',
                    'url': '/admin/archives/personnel/'
                },
                {
                    'name': '以人搜图',
                    'icon': 'fa fa-address-card',
                    'url': '/v1/archives/search_person/'
                }
            ],
        },
        {
            'name': '图像搜索',
            'icon': 'fa fa-search',
            'url': '/v1/device/search_image/'
        },
        {
            'name': '门禁管理',
            'icon': 'fa fa-building',
            'models': [
                {
                    'name': '门禁列表',
                    'icon': 'fa fa-building',
                    'url': '/admin/monitor/restrictedarea/'
                },
                {
                    'name': '门禁通行',
                    'icon': 'fas fa-person-booth',
                    'url': '/admin/archives/accessdiscover/'
                },
                {
                    'name': '人员名单',
                    'icon': 'fas fa-child',
                    'url': '/admin/monitor/areamonitorpersonnel/'
                }
            ]
        },
        {
            'name': '重点车辆',
            'icon': 'fa fa-car',
            'models': [
                {
                    'name': '重点车辆',
                    'icon': 'fa fa-car',
                    'url': '/admin/monitor/vehiclemonitor/'
                },
                {
                    'name': '车辆报警',
                    'icon': 'fas fa-exclamation-triangle',
                    'url': '/admin/monitor/vehiclemonitordiscover/'
                }
            ]
        },
        {
            'name': '机动车管理',
            'icon': 'fa fa-bus',
            'url': '/admin/device/vehicle/'
        },
        {
            'name': '非机动车管理',
            'icon': 'fa fa-bicycle',
            'url': '/admin/device/motor/'
        },
        {
            'name': '设备管理',
            'icon': 'fab fa-whmcs',
            'url': '/admin/device/deviceinfo/'
        },
        {
            'name': '日志报警',
            'icon': 'fa fa-exclamation',
            'models': [
                {
                    'name': '事件报警',
                    'icon': 'fa fa-exclamation',
                    'url': '/admin/device/deviceoffline/'
                },
                {
                    'name': '系统日志',
                    'icon': 'far fa-bookmark',
                    'url': '/admin/admin/logentry/'
                },
            ],
        },
        {
            'name': '系统管理',
            'icon': 'fas fa-user-shield',
            'models': [
                {
                    'name': '用户管理',
                    'icon': 'fa fa-user',
                    'url': '/admin/auth/user/'
                },
                {
                    'name': '权限管理',
                    'icon': 'fas fa-shield-alt',
                    'url': '/admin/auth/permission/'
                },
                {
                    'name': '权限组管理',
                    'icon': 'fas fa-users',
                    'url': '/admin/auth/group/'
                },
                {
                    'name': '异步任务',
                    'icon': 'fas fa-user-shield',
                    'models': [
                        {
                            'name': '时钟',
                            'icon': 'fa fa-clock',
                            'url': '/admin/django_celery_beat/clockedschedule/'
                        },
                        {
                            'name': 'crontab',
                            'icon': 'fa fa-user-clock',
                            'url': '/admin/django_celery_beat/crontabschedule/'
                        },
                        {
                            'name': '间隔',
                            'icon': 'fa fa-stop',
                            'url': '/admin/django_celery_beat/intervalschedule/'
                        },
                        {
                            'name': '周期任务',
                            'icon': 'fa fa-business-time',
                            'url': '/admin/django_celery_beat/periodictask/'
                        },
                        {
                            'name': '事件',
                            'icon': 'fa fa-solar-panel',
                            'url': '/admin/django_celery_beat/solarschedule/'
                        },
                    ]
                }
            ]
        },

    ]
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'EXCEPTION_HANDLER': 'utils.exception_handler.custom_exception_handler',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
}

if DEBUG is False:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ('rest_framework.renderers.JSONRenderer',)

# Jwt配置
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    # 'JWT_ALLOW_REFRESH': False,
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_VERIFY_EXPIRATION': False
}

# Celery
CELERY_BROKER_URL = REDIS_SITE
CELERY_RESULT_BACKEND = REDIS_SITE
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 60  # result_expires
CELERY_TIMEZONE = TIME_ZONE  # 时区统一
CELERYD_MAX_TASKS_PER_CHILD = 20  # work数量
CELERYD_TASK_TIME_LIMIT = 60  # 任务超时时间
DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_ENABLE_UTC = False  # 是否启动UTC时间
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SCHEDULE = {
    'device_status': {  # 5分钟更新设备状态
        'task': 'device.tasks.device_status',
        'schedule': datetime.timedelta(minutes=5),
        'args': None
    },
    'device_count': {  # 1小时更新设备抓拍
        'task': 'device.tasks.device_count',
        'schedule': datetime.timedelta(hours=1),
        'args': None
    },
    'photo_cluster': {  # 每日 2:30 自动对昨天的数据进行归类处理
        'task': 'monitor.tasks.photo_cluster',
        'schedule': crontab(hour=2, minute=30),
        'args': None
    },
    'clear_disk': {  # 30分钟检查磁盘并清理过期数据
        'task': 'public.tasks.clear_disk',
        'schedule': datetime.timedelta(minutes=30),
        'args': None
    },
    'device_alarm': {  # 30s更新设备事件报警
        'task': 'device.tasks.device_alarm',
        'schedule': datetime.timedelta(seconds=30),
        'args': None
    },
}

# CORS 跨域配合
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

# 搜索服务器地址
SEARCH_SERVER_HOST = os.getenv('SEARCH_SERVER_HOST', 'http://192.168.2.95:5000')

# 回放视频搜索
SEARCH_VIDEO_HOST = os.getenv('SEARCH_VIDEO_HOST', 'http://192.168.2.111:3000')
VIDEO_HOST = os.getenv('VIDEO_HOST', 'http://192.168.2.111:10080')

# 视频实况转换服务器
SEARCH_REAL_TIME_HOST = os.getenv('SEARCH_REAL_TIME_HOST', 'http://192.168.2.89:8083')

# 双网卡配置
DOUBLE_NETWORK = os.getenv('DOUBLE_NETWORK', 0)  # 是否双网卡
D_REDIS_SERVER_HOST = os.getenv('D_REDIS_SERVER_HOST', '192.168.4.10')  # 双网卡IP
