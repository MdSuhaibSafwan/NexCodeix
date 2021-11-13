from django.db import models
from nexcodeix.common import uuid_without_dash


class BaseModel(models.Model):  
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid_without_dash)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
