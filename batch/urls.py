from django.urls import path
from . import views

urlpatterns = [
    path("all/", views.BatchListView.as_view(), ),
    path("create/", views.BatchCreateView.as_view(), ),
    path("update/<id>/", views.BatchUpdateView.as_view(), )
]
