from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from ..helpers import get_batch_by_id_or_None, get_batch_class_by_id_or_None


@sync_to_async
def get_batch(batch_id):
    return get_batch_by_id_or_None(batch_id)


@sync_to_async
def get_batch_class(class_id):
    return get_batch_class_by_id_or_None(class_id)


@sync_to_async
def get_user_by_token(token):
    try:
        obj = Token.objects.get(key=token)
    except ObjectDoesNotExist:
        return None

    return obj
