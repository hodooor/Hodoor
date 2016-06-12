from django import forms
from .models import Session, ProjectSeparation

class SessionForm(forms.ModelForm):
	class Meta:
		model = Session
		fields = ["duration"]

class ProjectSeparationForm(forms.ModelForm):
	class Meta:
		model = ProjectSeparation
		fields = ['project','time_spend','description','session']
		widgets = {
			'description': forms.Textarea(attrs={
				'cols': 50, 
				'rows': 2
			}),
			'session': forms.HiddenInput(),
		}