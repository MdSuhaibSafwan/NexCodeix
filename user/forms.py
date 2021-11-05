from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "__all__"


class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=150)
    password = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if not qs.exists():
            raise forms.ValidationError("Email like this is not Found")
        return email
