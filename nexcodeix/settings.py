import os
import environ
from pathlib import Path

env = environ.Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG") == "True"

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "nexcodeix.herokuapp.com"]

INSTALLED_APPS = [
    "channels",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main.apps.MainConfig',
    'batches.apps.BatchesConfig',
    'user.apps.UserConfig',
    'telegram.apps.TelegramConfig',

    'rest_framework',
    'rest_framework.authtoken',

    'crispy_forms',
    'bkash',

    'django_celery_beat',
    'django_celery_results',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nexcodeix.urls'

TEMPLATES_DIR1 = os.path.join(BASE_DIR, "Templates")
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR1, ],
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

AUTH_USER_MODEL = 'user.User'

WSGI_APPLICATION = 'nexcodeix.wsgi.application'
ASGI_APPLICATION = "main.channel_routers.application"

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get("DATABASE_NAME"),
            'HOST': os.environ.get("DATABASE_HOST"),
            'USER': os.environ.get("DATBASE_USER"),
            'PASSWORD': os.environ.get("DATABASE_PASSWORD"),
            'PORT': int(os.environ.get("DATABASE_PORT")),
        }
    }   

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get("DATABASE_NAME"),
#         'HOST': os.environ.get("DATABASE_HOST"),
#         'USER': os.environ.get("DATBASE_USER"),
#         'PASSWORD': os.environ.get("DATABASE_PASSWORD"),
#         'PORT': int(os.environ.get("DATABASE_PORT")),
#     }
# }   

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

APP_URL = os.environ.get("APP_URL", "https://nexcodeix.herokuapp.com")

# EMAIL SETTINGS

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# Bkash Settings 

BKASH_APP_KEY = "// bkash app base url"
BKASH_APP_SECRET = "// bkash app base url"
BKASH_APP_USERNAME = "// bkash app base url"
BKASH_APP_PASSWORD = "// bkash app base url"
BKASH_APP_VERSION = "// bkash app base url"
BKASH_APP_BASE_URL = "/user/bkash/"
BKASH_APP_PAYMENT_TOKEN_GRANT_URL = 'user/bkash/checkout/token/grant'
BKASH_APP_PAYMENT_CREATE_URL = '%s/%s/checkout/payment/create' % (BKASH_APP_BASE_URL, BKASH_APP_VERSION)
BKASH_APP_PAYMENT_EXECUTE_URL = '%s/%s/checkout/payment/execute' % (BKASH_APP_BASE_URL, BKASH_APP_VERSION)

LOGIN_URL = "/user/auth/login/"
LOGIN_REDIRECT_URL = "/"

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'


CRISPY_TEMPLATE_PACK = "bootstrap4"

STATIC_DIR1 = os.path.join(BASE_DIR, "static")
STATIC_DIRS = [
    STATIC_DIR1, 
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "static/media")
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
