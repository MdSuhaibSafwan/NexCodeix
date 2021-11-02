from django import forms
from .models import Batch, BatchUser
from django.contrib.auth import get_user_model

User = get_user_model()


class BatchForm(forms.ModelForm):

    class Meta:
        model = Batch
        fields = "__all__"


class BatchUserForm(forms.ModelForm):

    class Meta:
        model = BatchUser
        fields = "__all__"

