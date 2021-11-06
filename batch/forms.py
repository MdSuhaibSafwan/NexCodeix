from django import forms
from . import models
from django.utils import timezone
from .models import Batch, BatchUser, BatchClass, ClassMaterials
from django.contrib.auth import get_user_model

User = get_user_model()


def clean_days(self):
    days = list(self.cleaned_data.get("days"))
    print(days)
    for i in days:
        print(i)
        if i not in models.DAYS_LIST:
            print(i , " not in days list")
            raise forms.ValidationError("Days Should have a max length of 4 and should have days")

    return self.cleaned_data.get("days")


class BatchCreationForm(forms.ModelForm):   
    # start_date = forms.DateTimeField(label="Start Date")
    # end_date = forms.DateTimeField(label="End Date")

    class Meta:
        model = Batch
        # fields = "__all__"
        fields = ["name", "batch_category", "per_week", "days"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        try:
            if self.instance.update == True:
                print("Updating")
                return name
            else:
                print("Not Updating")
        except AttributeError as e:
            print(e)
        qs = Batch.objects.filter(name=name)
        if qs.exists():
            raise forms.ValidationError("Name with this Batch already Found")

        return name

    def clean_days(self):
        return clean_days(self)


class BatchUpdateForm(forms.ModelForm):   
    # start_date = forms.DateTimeField(label="Start Date")
    # end_date = forms.DateTimeField(label="End Date")

    class Meta:
        model = Batch
        # fields = "__all__"
        fields = ["name", "batch_category", "per_week", "days"]

    def clean_days(self):
        return clean_days(self)


class BatchUserForm(forms.ModelForm):

    class Meta:
        model = BatchUser
        fields = "__all__"

    def validate_unique(self):
        return super().validate_unique()

