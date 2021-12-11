from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from .models import Batch, BatchClass, ClassMaterials, BatchImportantAnouncement, ClassJoinedUser, DAYS_LIST, DAYS_NUMBER_LIST
from .tasks import create_batch_class_task
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from datetime import timedelta
from user.api.serializers import UserProfileSerializer

from django_celery_beat.models import PeriodicTask, CrontabSchedule

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()
channel_layer = get_channel_layer()

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
    date = instance.start_date
    time = instance.time_starts
    if created:
        crontab_obj, cron_created = CrontabSchedule.objects.get_or_create(day_of_month=date.day, month_of_year=date.month, 
                                                                    hour=time.hour-1)
        obj = PeriodicTask.objects.create(name=f"batch_{instance.id}", crontab=crontab_obj, args=[instance, ],
                                         task="batches.tasks.send_mail_for_class", one_off=True)
        print("Periodic task Created for the batch ", obj)
        return obj
    
    else:
        crontab_obj, cron_created = CrontabSchedule.objects.get_or_create(day_of_month=date.day, month_of_year=date.month, 
                                                                    hour=time.hour-1)        
        try:
            obj = PeriodicTask.objects.get(name=f"batch_{instance.id}")
        except ObjectDoesNotExist:
            return

        obj.crontab = crontab_obj
        obj.save()
        print("PERIODIC TASK CRONTAB UPDATED.")
        return obj


@receiver(signal=post_save, sender=BatchImportantAnouncement)
def create_periodic_task_for_anouncement(sender, instance, created, **kwargs):
    if created:
        date = instance.end_date; hour = date.hour; minute = date.minute
        date = date.date()
        month = date.month; day = date.day
        crontab_obj, cron_created = CrontabSchedule.objects.get_or_create(day_of_month=day, 
                                    month_of_year=month, hour=hour, minute=minute)

        obj = PeriodicTask.objects.create(name=f"del_anouncement_{instance.id}", crontab=crontab_obj, 
                                args=[instance, ], task="batches.tasks.delete_anouncement", one_off=True)

        return obj


@receiver(signal=post_save, sender=ClassJoinedUser)
def send_channel_layer_for_class_joined_user(sender, instance, created, **kwargs):
    if created:
        data = {}
        data["id"] = str(instance.id)
        data["msg_type"] = "SRJ"  # Student Requested Joining
        user_data = UserProfileSerializer(instance.user).data
        
        user_data["id"] = str(user_data["id"])
        data["user"] = user_data
        
        class_id = "class_room_" + str(instance.batch_class.id)

        async_to_sync(channel_layer.group_send)(
            class_id, 
            {
                "type": "send.notification",
                "text": data
            }
        )

