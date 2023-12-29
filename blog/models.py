from django.db import models
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField

User = get_user_model()


class Article(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
	title = models.CharField(max_length=100)
	content = HTMLField()
	date_created = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title
