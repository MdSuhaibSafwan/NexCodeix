from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BatchClass, ClassMaterials


@receiver(signal=post_save, sender=BatchClass)
def create_class_materials(sender, instance, created, **kwargs):
    if created:
        obj = ClassMaterials.objects.create(batch_class=instance)
        return obj
    
    return False
