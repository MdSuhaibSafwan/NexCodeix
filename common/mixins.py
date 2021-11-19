from django.shortcuts import redirect
from django.conf import settings


class UserVerifiedMixin:

    def dispatch(self, request, *args, **kwargs):
        curr_user = request.user
        if not curr_user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        if not curr_user.is_verified:
            print("User is not Verified")
            return False

        return True
        