from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailSubscriber(models.Model):
	email = models.EmailField()
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email


class MessageQuery(models.Model):
	name = models.CharField(max_length=100, )
	email = models.EmailField()
	subject = models.TextField()
	description = models.TextField()
	has_responded = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name
