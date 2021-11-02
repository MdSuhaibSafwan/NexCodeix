from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nexcodeix.settings")

REDIS_URL = settings.REDIS_URL

app = Celery("nexcodeix")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = REDIS_URL

app.autodiscover_tasks()
