from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import BatchClass, ClassMaterials
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def create_batch_class_task(**kwargs):
    batch = BatchClass.objects.create(**kwargs)
    return batch


@shared_task
def send_mail_for_class(batch_class):
    print("Inside Task ", batch_class)
    class_material = ClassMaterials.objects.create(batch_class=batch_class)
    batch = batch_class.batch
    emails = batch.user.all().values_list("email")
    
    recipient_list = list(emails)

    send_mail(
        subject="Reminder of Class",
        message="It is to remind you that class will be held exactly after 1 Hour",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
    )

    print("SENT MAILS FOR REMINDER OF BATCH CLASS TO ", recipient_list)

