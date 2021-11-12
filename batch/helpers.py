from django.contrib.auth import get_user_model
from .models import Batch, BatchClass

User = get_user_model()


def get_next_batch_classes(user):
    batches = user.batches.all()
    batch_class_qs = BatchClass.objects.none()

    for batch in batches:
        batch_class_qs |= batch.classes.filter(started=False)

    return batch_class_qs
