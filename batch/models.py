from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

BATCH_CATEGORY = (
    ("PY", "PYTHON"),
    ("DJ", "DJANGO"),
    ("FS", "FLASK"),

)


class Batch(models.Model):
    name = models.CharField(max_length=50)
    batch_category = models.CharField(max_length=2, choices=BATCH_CATEGORY)

    user = models.ManyToManyField(User, through="BatchUser", related_name="batches")

    started = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class BatchUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch.name
