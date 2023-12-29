from django.contrib import admin
from .models import Article, ArticleImage
from .forms import ArticleForm


class ArticleAdmin(admin.ModelAdmin):
	form = ArticleForm
	list_display = ["title", ]


class ArticleImageAdmin(admin.ModelAdmin):
	list_display = ["article__title", ]
	

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleImage)
