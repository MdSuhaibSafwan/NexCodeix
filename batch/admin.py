from django.contrib import admin
from .models import Batch, BatchUser


class BatchAdmin(admin.ModelAdmin):
    list_display = ["name", "days", "per_week", "time_starts", "time_ends"]


admin.site.register(Batch, BatchAdmin)
admin.site.register(BatchUser)
