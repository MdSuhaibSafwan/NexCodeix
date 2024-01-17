from django.shortcuts import render
from django.views.generic import TemplateView


class IndexPage(TemplateView):
	template_name = "blog/index.html"



class ProjectDetailPage(TemplateView):
	template_name = "blog/project-detail.html"

