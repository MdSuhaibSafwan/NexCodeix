from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import BatchClass


@shared_task
def create_batch_class_task(**kwargs):
    batch = BatchClass.objects.create(**kwargs)
    return batch
