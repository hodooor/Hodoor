from django import forms
from .models import Session, ProjectSeparation

class SessionForm(forms.ModelForm):
	class Meta:
		model = Session
		fields = ["duration"]

class ProjectSeparationForm(forms.ModelForm):
	class Meta:
		model = ProjectSeparation
		fields = ['project', 'description', 'time_spend']