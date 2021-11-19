from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from .models import UserVerificationOTP

@shared_task
def add(x, y):
    return x + y


@shared_task
def make_verification_token_expired(token_obj=None, token=None):
    if not token_obj:
        try:
            token_obj = UserVerificationOTP.objects.get(token=token)
        except ObjectDoesNotExist as e:
            print("Couldn't Find Token ", e)
            return
    token_obj.expired = True
    token_obj.save()
