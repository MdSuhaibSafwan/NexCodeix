from django.contrib.auth import get_user_model
from .models import Batch, BatchClass
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured


User = get_user_model()


def get_next_batch_classes(user):
    batches = user.batches.all()
    batch_class_qs = BatchClass.objects.none()

    for batch in batches:
        batch_class_qs |= batch.classes.filter(started=False)

    return batch_class_qs


def get_tomorrow_batch_classes(qs=None, user=None):
    if (qs is None) and (user is None):
        raise ImproperlyConfigured("Both qs and user cannot be None")

    time_now = timezone.now()
    time_tomorrow = time_now + timedelta(days=1)

    if qs is not None:
        qs = qs.filter(start_date__gt=time_now, start_date__date=time_tomorrow.date())
        return qs

    qs = get_next_batch_classes(user)
    qs = qs.filter(start_date__gt=time_now, start_date__date=time_tomorrow)
    return qs


def get_today_batch_classes(qs=None, user=None):

    if (qs is None) and (user is None):
        raise ImproperlyConfigured("Both qs and user cannot be None")

    time_now = timezone.now()

    if qs is not None:
        qs = qs.filter(
            start_date__date=time_now.date(),
        )
        return qs

    qs = get_next_batch_classes(user)
    qs = qs.filter(start_date__date=time_now.date())
    return qs
