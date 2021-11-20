from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import BatchClass, ClassMaterials


@shared_task
def create_batch_class_task(**kwargs):
    batch = BatchClass.objects.create(**kwargs)
    return batch


@shared_task
def send_mail_for_class(batch_class):
    print("Inside Task ", batch_class)
    class_material = ClassMaterials.objects.create(batch_class=batch_class)
    return class_material

