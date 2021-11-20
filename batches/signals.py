from django.contrib.auth import get_user_model
from .models import Batch, BatchClass, ClassMaterials, DAYS_LIST, DAYS_NUMBER_LIST
from .tasks import create_batch_class_task
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import timedelta

from django_celery_beat.models import PeriodicTask, CrontabSchedule

User = get_user_model()


@receiver(signal=post_save, sender=Batch)
def trigger_task_for_creating_batch_class(sender, instance, created, **kwargs):
    if created:
        start_date = instance.start_date
        end_date = instance.end_date
        t1 = instance.time_starts
        t2 = instance.time_ends
        time_del = timedelta(days=1)
        week_days = list(instance.days)
        lst = []
        for i in week_days:
            lst.append(DAYS_NUMBER_LIST[i])

        print("WEEK DAYS ", lst)
        

        while True:
            print("START DATE ", start_date, start_date.weekday())
            if start_date.weekday() in lst:
                obj = create_batch_class_task(day=start_date.weekday(), start_date=start_date, batch=instance, time_starts=t1, time_ends=t2)
                # obj = BatchClass.objects.create(day=start_date.weekday(), start_date=start_date, 
                #                                 batch=instance, time_starts=t1, time_ends=t2)

                print("Creating Batch Class ", obj.start_date)
            start_date += time_del
            if start_date > end_date:
                break


@receiver(signal=post_save, sender=BatchClass)
def create_periodic_task_for_reminder_of_class(sender, instance, created, **kwargs):
    if created:
        date = instance.start_date
        time = instance.time_starts
        obj, cron_created = CrontabSchedule.objects.get_or_create(day_of_month=date.day, month_of_year=date.month, 
                                                                    hour=time.hour-1)
        obj = PeriodicTask.objects.create(name=f"batch_{instance.id}", crontab=obj, args=[instance, ],
                                         task="batches.tasks.send_mail_for_class", one_off=True)
        print("Periodic task Created for the batch ", obj)
        return obj
