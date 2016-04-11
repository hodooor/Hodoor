from django.db import models
from django.contrib.auth.models import User

class Session(models.Model):
	'''
	Session is from login swipe to logout swipe and can have one or 
	more breaks
	'''

	user = models.ForeignKey(User)
	duration = models.DurationField(null = True)

	description = models.CharField(max_length = 100, null = True) 
	modified = models.BooleanField(default = False) 

class Swipe(models.Model):
	'''
	Swipes are individual key scans of each user
	'''

	SWIPE_TYPES = (
					("IN","Incoming"),
					("OUT","Outcoming"),
					("TBR","To Break"),
					("FBR","From Break")		
	)

	user = models.ForeignKey(User)
	datetime = models.DateTimeField("Datetime of swipe")

	swipe_type = models.CharField(max_length=3, choices = SWIPE_TYPES)

	session = ForeignKey(Session)
	def __str__(self):
		return str(self.id) + " " + self.user.username + 
		" " + self.swipe_type