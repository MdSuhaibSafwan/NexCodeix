from django import forms
from . import models
from .models import Batch, BatchUser
from django.contrib.auth import get_user_model

User = get_user_model()


class BatchForm(forms.ModelForm):

    class Meta:
        model = Batch
        # fields = "__all__"
        exclude = ["user", ]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        qs = Batch.objects.filter(name=name)
        if qs.exists():
            raise forms.ValidationError("Name with this Batch already Found")

        return name

    def clean_days(self):
        days = list(self.cleaned_data.get("days"))
        for i in days:
            if i not in models.DAYS_LIST:
                raise forms.ValidationError("Days Should have a max length of 4 and should have days")

        return days

    def clean_time_ends(self):
        time_starts = self.cleaned_data.get("time_starts")
        time_ends = self.cleaned_data.get("time_ends")

        return time_ends


class BatchUserForm(forms.ModelForm):

    class Meta:
        model = BatchUser
        fields = "__all__"

