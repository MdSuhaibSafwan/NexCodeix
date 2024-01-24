import json
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from project.models import Project
from django.http import JsonResponse
from subscription.models import MessageQuery


class IndexPage(ListView):
	template_name = "blog/index.html"
	context_object_name = "projects"


	def get_queryset(self):
		queryset = Project.objects.get_top_projects()
		return queryset

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		print(data)
		return data


class ProjectDetailPage(TemplateView):
	template_name = "blog/project-detail.html"



def create_query(request):
	data = json.loads(request.body.decode("utf-8"))
	print(data)

	mq_obj = MessageQuery(
		name=data.get("name", None),
		email=data.get("email", None),
		subject=data.get("subject", None),
		description=data.get("message", None),
	)
	try:
		mq_obj.save()
	except Exception as e:
		print("Error ", e)
		error_data = {
			"status": 400,
			"message": "Something went wrong please try again",
			'api-response': e,
		}
		return JsonResponse(error_data, safe=False)

	success_data = {
		"status": 200,
		"message": "Query completed",
	}
	return JsonResponse(success_data, safe=False)

