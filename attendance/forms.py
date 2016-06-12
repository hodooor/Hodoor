from django import forms
from .models import Session, ProjectSeparation, Swipe
from django.contrib.admin.widgets import AdminDateWidget 

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
class SwipeEditForm(forms.ModelForm):
	class Meta:
		model = Swipe
		fields = ["datetime"]
		widget = {"datetime": AdminDateWidget }