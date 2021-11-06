from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserForm(forms.ModelForm):
    email = forms.EmailField(max_length=150)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter a Strong password.",
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "password2"]

    def clean_password2(self):
        p1 = self.cleaned_data.get("password")
        p2 = self.cleaned_data.get("password2")
        if p1 != p2:
            raise forms.ValidationError("Both the password did not match")

        return p2


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=150)
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
