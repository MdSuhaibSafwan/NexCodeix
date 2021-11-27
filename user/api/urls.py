from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login_api_view, name="Login_Api_View"),
    path("registration/", views.registration_api_view, name="Register_Api_View"),

]

