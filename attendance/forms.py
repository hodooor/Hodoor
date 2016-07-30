from django import forms
from .models import Session, ProjectSeparation, Swipe
from django.contrib.admin.widgets import AdminDateWidget 
from datetimewidget.widgets import DateTimeWidget
from datetime import timedelta

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

	def clean_time_spend(self):
		data = self.cleaned_data["time_spend"]
		if data <= timedelta(0):
			raise forms.ValidationError("Can't be zero or negative")
		return data

	def clean(self):
		cleaned_data = super(ProjectSeparationForm, self).clean()
		time_spend = cleaned_data.get("time_spend")
		session = cleaned_data.get("session")
		if time_spend and session:
			if(time_spend > cleaned_data.get("session").session_duration()):
				msg = "Time spend more then not assigned time"
				self.add_error('time_spend', msg)


class SwipeEditForm(forms.ModelForm):
	class Meta:
		model = Swipe
		fields = ["datetime"]
	
	def clean_datetime(self):
		data = self.cleaned_data["datetime"] #data passed to form
		this_swipe = self.instance
		last_swipe_datetime = this_swipe.get_last_swipe_same_user().datetime
		next_swipe_datetime = this_swipe.get_next_swipe_same_user().datetime
		
		if last_swipe_datetime < data < next_swipe_datetime:
			return  data
		else:
			raise forms.ValidationError("Conflicting datetime.")