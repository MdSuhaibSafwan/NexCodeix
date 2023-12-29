from django.contrib import admin
from .models import Article, ArticleImage


class ArticleAdmin(admin.ModelAdmin):
	list_display = ["title", ]


class ArticleImageAdmin(admin.ModelAdmin):
	list_display = ["article__title", ]
	

admin.site.register(Article)
admin.site.register(ArticleImage)
