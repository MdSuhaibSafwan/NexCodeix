from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("verify/", views.verify_user, ),
    path("auth/registration/", views.UserRegistrationView.as_view(), ),
    path("auth/login/", LoginView.as_view(template_name="user/auth/login.html"), ),
]
