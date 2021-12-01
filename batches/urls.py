from django.urls import path
from . import views

urlpatterns = [
    path("all/", views.BatchListView.as_view(), ),
    path("create/", views.BatchCreateView.as_view(), ),
    path("update/<id>/", views.BatchUpdateView.as_view(), ),


    path("join/<id>/", views.JoinABatchView.as_view(), name="join_a_batch_view"),
    path("joining/cancel/<batch_id>/", views.cancel_batch_join_request, name="cancels_batch_joining"),

    path("user/classes/", views.UserClassesView.as_view(), name="user_classes"),
    path("user/class/<class_id>/view/", views.ClassDetailView.as_view(), name="class_detail_view"),

]
