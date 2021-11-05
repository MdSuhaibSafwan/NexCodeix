from django.urls import path
from . import views

urlpatterns = [
    path("verify/<id>/", views.verify_user, ),
    path("registration/", views.UserRegistrationView.as_view(), ),
    path("login/", views.UserLoginView.as_view(), ),
]
