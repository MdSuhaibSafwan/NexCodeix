from django.contrib.auth import mixins
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages


class LoginRequiredAndVerificationMixin:
    
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        if not user.is_verified:
            messages.warning(request, "User is not Verified")
            return redirect("/")

        return super().dispatch(request, *args, **kwargs)
    

def login_and_verification_required(function):

    def wrap(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        if not user.is_verified:
            messages.warning(request, "User is not Verified")
            return redirect("/")

        return function(request, *args, **kwargs)

    return wrap
