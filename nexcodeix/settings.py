import os
import environ
from pathlib import Path

env = environ.Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-nuc1v(8w&9ke6ekkyhqy_@a8(mzeeyy73r_)tow_al%ebt9u2w'

DEBUG = os.environ.get("DEBUG") == "True"

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "nexcodeix.herokuapp.com"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main.apps.MainConfig',
    'batch.apps.BatchConfig',
    'user.apps.UserConfig',
    'telegram.apps.TelegramConfig',

    'crispy_forms',
    'rest_framework',

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

# if DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.environ.get("DATABASE_NAME"),
#             'HOST': os.environ.get("DATABASE_HOST"),
#             'USER': os.environ.get("DATBASE_USER"),
#             'PASSWORD': os.environ.get("DATABASE_PASSWORD"),
#             'PORT': int(os.environ.get("DATABASE_PORT")),
#         }
#     }   

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")

STATIC_DIR1 = os.path.join(BASE_DIR, "static")
STATIC_DIRS = [
    STATIC_DIR1, 
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "static/media")
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
