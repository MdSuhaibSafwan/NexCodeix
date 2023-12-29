from django import forms
from .models import Article
from tinymce.widgets import TinyMCE 


class TinyMCEWidget(TinyMCE): 
    def use_required_attribute(self, *args): 
        return False


class ArticleForm(forms.ModelForm):
	content = forms.CharField(
		widget=TinyMCEWidget(
			attrs={'required': False, 'rows': 30, 'cols': 30}
		)
	)

	class Meta:
		model = Article
		fields = "__all__"
