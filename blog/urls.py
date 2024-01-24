from django.urls import path
from . import views

urlpatterns = [
	path("", views.IndexPage.as_view(), name='index-page'),
	path("project-detail/", views.ProjectDetailPage.as_view(), name="project-detail-page"),
	path("send-query/", views.create_query, name="send-query")
]
