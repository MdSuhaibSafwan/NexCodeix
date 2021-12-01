from datetime import timedelta
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from nexcodeix.common import uuid_without_dash
from common.models import BaseModel

User = get_user_model()

BATCH_CATEGORY = (
    ("PY", "PYTHON"),
    ("DJ", "DJANGO"),
    ("FS", "FLASK"),
)

DAYS_LIST = {
    "S": "Sunday",
    "M": "Monday",
    "T": "Tuesday",
    "W": "Wednesday",
    "U": "Thursday",  # U --> Thursday
    "F": "Friday",
    "Z": "Saturday",  # Z --> Saturday
} 

DAYS_NUMBER_LIST = {
    "S": 6,
    "M": 0,
    "T": 1,
    "W": 2,
    "U": 3,  # U --> Thursday
    "F": 4,
    "Z": 5,  # Z --> Saturday
} 


class Batch(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid_without_dash)
    name = models.CharField(max_length=50)
    batch_category = models.CharField(max_length=2, choices=BATCH_CATEGORY)

    user = models.ManyToManyField(User, through="BatchUser", related_name="batches")

    started = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    per_week = models.IntegerField(default=2)
    days = models.CharField(max_length=4, null=True, blank=True)
    time_starts = models.TimeField(null=True, blank=True)
    time_ends = models.TimeField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created", ]

    def __str__(self):
        return self.name

    def validate_started(self):
        time_now = timezone.now()
        start_date = self.start_date
        started = self.started

        if (time_now < start_date) and (started == True):
            raise ValidationError("Time did not reach upto the point to start")

    def validate_days(self):
        days = self.days
        if days is None:
            return None

        days = list(days)
        for i in days:
            if i not in DAYS_LIST:
                raise ValidationError("This should be a day Word")

        return True        

    def save(self, *args, **kwargs):
        if self.started and self.start_date:
            self.validate_days()
            self.validate_started()

        return super().save(*args, **kwargs)
        


class BatchImportantAnouncement(BaseModel):
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    anouncement = models.TextField()
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.batch} --> {self.anouncement}"

    def save(self, *args, **kwargs):
        end_date = self.end_date
        if not end_date:
            self.end_date = timezone.now() + timedelta(days=1)

        return super().save(*args, **kwargs)


class BatchUser(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    verified_for_batch = models.BooleanField(default=False)

    user_name = models.CharField(max_length=100, null=True)

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "batch"]

    def __str__(self):
        return self.batch.name

    def validate_user(self):
        if not self.user.is_verified:
            raise ValidationError("User not Verified")

        return True

    def save(self, *args, **kwargs):
        self.validate_user()
        return super().save(*args, **kwargs)

    @property
    def is_verified(self):
        return self.verified_for_batch
        

class BatchClass(BaseModel):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="classes")

    day = models.CharField(max_length=4, null=True, blank=True)
    started = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    time_starts = models.TimeField(null=True, blank=True)
    time_ends = models.TimeField(null=True, blank=True)

    last_updated = models.DateTimeField(auto_now=True)


class ClassMaterials(BaseModel):
    batch_class = models.OneToOneField(BatchClass, on_delete=models.CASCADE)
    video = models.FileField(upload_to="batch/class/video", null=True, blank=True)
    git_link = models.CharField(max_length=2040, blank=True, null=True)
    files = models.FileField(upload_to="batch/class/files", blank=True, null=True)

    def __str__(self):
        return self.batch_class.batch.name + " Materials"


class ClassJoinedUser(BaseModel):
    STATUS = (
        ("J", "JOINED"),
        ("P", "PENDING"),
        ("N", "NOT JOINED")
    )
    batch_class = models.ForeignKey(BatchClass, on_delete=models.CASCADE, related_name="joined_users")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS, default="P")

    class Meta:
        unique_together = ["batch_class", "user"]

    def __str__(self):
        return self.user.email + " | Joined"
