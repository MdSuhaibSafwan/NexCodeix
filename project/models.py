from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectManager(models.Manager):

	def get_top_projects(self):
		queryset = self.get_queryset()
		return queryset


class Project(models.Model):
	name = models.CharField(max_length=100, unique=True)
	proj_type = models.CharField(verbose_name="Project Type", max_length=10)
	description = models.TextField(verbose_name="Project Description", )
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	objects = ProjectManager()

	def get_image(self):
		image = self.projectimage_set.first()
		if image is None:
			return None

		return image.image.url


class ProjectImage(models.Model):
	project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
	image = models.ImageField(upload_to="projects/")

	def __str__(self):
		return self.project.name
