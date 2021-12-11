from django import template
from django.core.exceptions import ObjectDoesNotExist
from ..models import ClassJoinedUser

register = template.Library()


@register.simple_tag(name="has_user_joined_class")
def has_user_joined_class(user, class_object):
    try:
        obj = ClassJoinedUser.objects.get(user=user, batch_class=class_object)
    except ObjectDoesNotExist:
        return "NOT JOINED"
    STATUS = dict(ClassJoinedUser.STATUS)
    return STATUS[obj.status]


# register.filter("has_user_joined_class", has_user_joined_class)
