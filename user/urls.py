from django.urls import path
from django.urls.conf import include
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("verify/", views.verify_user, ),
    path("verify/resend_token/", views.resend_another_verification_token, ),

    path("auth/registration/", views.UserRegistrationView.as_view(), ),
    path("auth/login/", LoginView.as_view(template_name="user/auth/login.html"), ),

    path("bkash/", include("bkash.urls"), ),
]
