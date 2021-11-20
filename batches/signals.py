from django.contrib.auth import get_user_model
from .models import Batch, BatchClass, ClassMaterials
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import timedelta

User = get_user_model()

@receiver(signal=post_save, sender=Batch)
def trigger_task_for_creating_batch_class(sender, instance, created, **kwargs):
    if created:
        start_date = instance.start_date
        end_date = instance.end_date
        t1 = instance.time_starts
        t2 = instance.time_ends

        while True:
            time_del = timedelta(days=1)
            week_days = [1, 2, 3]
            if start_date.weekday() in week_days:
                obj = BatchClass.objects.create(day=start_date.weekday(), start_date=start_date, batch=instance,
                                                time_starts=t1, time_ends=t2)
                print("Creating Batch Class ", obj)
            start_date += time_del
            if start_date > end_date:
                break


