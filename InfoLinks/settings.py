import os
import environ
from pathlib import Path

env = environ.Env().read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG") == "True"

ALLOWED_HOSTS = ["127.0.0.1", "localhost", ]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blog.apps.BlogConfig',
    'user.apps.UserConfig',
    'project.apps.ProjectConfig',
    'subscription.apps.SubscriptionConfig',
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

ROOT_URLCONF = 'InfoLinks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "Templates"), ],
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

WSGI_APPLICATION = 'InfoLinks.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'nexcodeix.sqlite3',
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

AUTH_USER_MODEL = "user.User"

# TINYMCE_DEFAULT_CONFIG = {
#     'cleanup_on_startup': True,
#     'custom_undo_redo_levels': 20,
#     'selector': 'textarea',
#     'theme': 'silver',
#     'plugins': '''
#             textcolor save link image media preview codesample contextmenu
#             table code lists fullscreen  insertdatetime  nonbreaking
#             contextmenu directionality searchreplace wordcount visualblocks
#             visualchars code fullscreen autolink lists  charmap print  hr
#             anchor pagebreak
#             ''',
#     'toolbar1': '''
#             fullscreen preview bold italic underline | fontselect,
#             fontsizeselect  | forecolor backcolor | alignleft alignright |
#             aligncenter alignjustify | indent outdent | bullist numlist table |
#             | link image media | codesample |
#             ''',
#     'toolbar2': '''
#             visualblocks visualchars |
#             charmap hr pagebreak nonbreaking anchor |  code |
#             ''',
#     'contextmenu': 'formats | link image',
#     'menubar': True,
#     'statusbar': True,

#     "file_picker_callback": """function (cb, value, meta) {
#         var input = document.createElement("input");
#         input.setAttribute("type", "file");
#         if (meta.filetype == "image") {
#             input.setAttribute("accept", "image/*");
#         }
#         if (meta.filetype == "media") {
#             input.setAttribute("accept", "video/*");
#         }

#         input.onchange = function () {
#             var file = this.files[0];
#             var reader = new FileReader();
#             reader.onload = function () {
#                 var id = "blobid" + (new Date()).getTime();
#                 var blobCache = tinymce.activeEditor.editorUpload.blobCache;
#                 var base64 = reader.result.split(",")[1];
#                 var blobInfo = blobCache.create(id, file, base64);
#                 blobCache.add(blobInfo);
#                 cb(blobInfo.blobUri(), { title: file.name });
#             };
#             reader.readAsDataURL(file);
#         };
#         input.click();
#     }"""

    
# }


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
