from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import UserVerificationOTP
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_celery_beat.models import PeriodicTask, CrontabSchedule

User = get_user_model()


@receiver(signal=post_save, sender=User)
def send_mail_to_user_account(sender, instance, created, **kwargs):
    if created:
        print("CREATING VERIFICATION TOKEN")
        obj = UserVerificationOTP.objects.create(user=instance)
        # render_to_string("", context={"verification_token": str(obj.token)})
        print("SENDING VERIFICATION MAIL TO NEW USER")
        message = f"Please Verify Your Account at {settings.APP_URL}/user/verify/?id={obj.token}"
        send_mail(
            subject="Verify Account",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email, ],
        )
        print("VERIFICATION MAIL SENT SUCCESSFULLY")


@receiver(signal=post_save, sender=UserVerificationOTP)
def create_task_for_expiry(sender, instance, created, **kwargs):
    if created:
        tm = instance.date_created
        minute = tm.minute
        hour = tm.hour
        day = tm.date().day

        schedule = CrontabSchedule.objects.create(minute=minute+5, hour=hour, day_of_month=day)

        obj = PeriodicTask.objects.create(name=f"verification_{instance.id}", crontab=schedule, one_off=True,
                    task="user.tasks.make_verification_token_expired", args=[instance, instance.token])
        return obj
