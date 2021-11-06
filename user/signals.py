from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(signal=post_save, sender=User)
def send_mail_to_user_account(sender, instance, created, **kwargs):
    if created:
        print("Inside Signals of user")