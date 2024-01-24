from django.contrib import admin
from .models import MessageQuery, EmailSubscriber


admin.site.register(MessageQuery)
admin.site.register(EmailSubscriber)
