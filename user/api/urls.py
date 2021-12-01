from django.urls import path
from django.urls.conf import include
from . import views


urlpatterns = [
    path("login/", views.login_api_view, name="Login_Api_View"),
    path("registration/", views.registration_api_view, name="Register_Api_View"),
    path("profile/", views.UserProfileAPIView.as_view(), name="User_Profile_API_View"),
    path("rest_auth/", include("rest_framework.urls")),
]

