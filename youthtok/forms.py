from django import forms
from .models import *


class CommentForm(forms.ModelForm):
	content = forms.CharField(
		label= '',
		widget=forms.TextInput(attrs={
			'row': '12',
			'placeholder': 'Say something...',
		})
		)

	class Meta:
		model = Comment
		fields = ['content']

class Video_form(forms.ModelForm):
	class Meta:
		model = Video
		fields = ("caption", "video")


