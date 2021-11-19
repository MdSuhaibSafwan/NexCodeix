from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from .models import UserVerificationOTP

@shared_task
def add(x, y):
    return x + y


@shared_task
def make_verification_token_expired(token_obj=None, token=None):
    print(token_obj, token)

    if token_obj is None:
        obj = UserVerificationOTP.objects.get(token=token)

    obj.expired = True
    obj.save()
    return obj
