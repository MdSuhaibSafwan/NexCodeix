from django.contrib import admin
from .models import Batch, BatchClass, ClassMaterials, BatchUser, BatchImportantAnouncement

admin.site.register(Batch)
admin.site.register(BatchClass)
admin.site.register(ClassMaterials)
admin.site.register(BatchUser)
admin.site.register(BatchImportantAnouncement)
