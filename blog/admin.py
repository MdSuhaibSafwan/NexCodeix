from django.contrib import admin
from .models import Article
from .forms import ArticleForm


class ArticleAdmin(admin.ModelAdmin):
	form = ArticleForm
	list_display = ["title", ]
	

admin.site.register(Article, ArticleAdmin)
