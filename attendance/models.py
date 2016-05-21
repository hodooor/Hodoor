from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
import datetime

class Session(models.Model):
	'''
	Session is from login swipe to logout swipe and can have one or 
	more breaks
	'''

	user = models.ForeignKey(User)
	duration = models.DurationField(null = True, blank = True)

	description = models.CharField(
		max_length = 100, 
		null = True, 
		blank = True
	)

	modified = models.BooleanField(default = False) 
	def num_of_breaks (self):
		'''
		Returns number of completed breaks during session
		'''

		obr = self.swipe_set.filter(swipe_type = "OBR")
		fbr = self.swipe_set.filter(swipe_type = "FBR")
		if len(obr) != len(fbr):
			print("Some breaks are not complete")
		return len(fbr)

	def breaks_duration (self):
		'''
		Returns timedelta duration of all breaks
		'''
		
		obr = self.swipe_set.filter(swipe_type = "OBR")
		fbr = self.swipe_set.filter(swipe_type = "FBR")

		duration = datetime.timedelta(0)

		for obr_object, fbr_object  in zip(obr,fbr):
			duration += fbr_object.datetime - obr_object.datetime
		
		return duration
	def session_duration_overall (self):
		'''
		Returns time delta duration of session(including breaks)
		'''

		login_datetime = self.swipe_set.get(swipe_type = "IN").datetime
		logout_datetime = self.swipe_set.get(swipe_type = "OUT").datetime

		return logout_datetime - login_datetime

	def session_duration(self):
		'''
		Returns time delta duration of session(excluding breaks)
		'''

		return self.session_duration_overall() - self.breaks_duration() 

	def __str__(self):
		return str(self.id) + " " + str(self.user)

class Swipe(models.Model):
	'''
	Swipes are individual key scans of each user
	'''

	SWIPE_TYPES = (
					("IN","Login"),
					("OUT","Logout"),
					("OBR","On Break"),
					("FBR","From Break"),
					("OTR","On Trip"),
					("FTR","From Trip")		
	)

	user = models.ForeignKey(User)
	datetime = models.DateTimeField("Datetime of swipe")

	swipe_type = models.CharField(max_length=3, choices = SWIPE_TYPES)

	session = models.ForeignKey(Session,
		null = True, 
		blank = True, 
		on_delete = models.SET_NULL,
		)
	source = models.CharField(max_length = 5,null = True, blank = True)

	def __str__(self):
		return str(self.id) + " " + self.user.username + " " + self.swipe_type

class Key(models.Model):
	'''
	Saves information data about keys.
	'''
	id = models.CharField(max_length = 10, primary_key = True) 
	key_type = models.CharField(max_length = 4, null = True, blank = True)
	user = models.ForeignKey(User)

	def __str__(self):
		return self.id + " " + self.user.username + " " + self.key_type





@receiver(post_save, sender = Swipe)
def post_process_swipes(sender=Swipe, **kwargs):
	if(kwargs['created']): # trigering only when swipe was created
		
		print(" post_process_swipes trigered")
		#swipe object that was just created
		created_swipe = kwargs["instance"] 

		#open new session 
		if(created_swipe.swipe_type == "IN"):
			print("created in swipe")
			#session has same user as swipe
			sess = Session(user = created_swipe.user)
			sess.save()

			#swipe is related to session 
			created_swipe.session = sess
			created_swipe.save()

		#updated oppened session
		else:
			print("session updated")
			sess = Session.objects.filter(user = created_swipe.user)
			sess = sess.exclude(swipe__swipe_type = "OUT") #session without OUT swipe (open session)

			if(len(sess) == 1):
				sess = sess[0]
			else:
				#this should not be possible 
				raise ValueError('More Opened Sessions')
					
			created_swipe.session = sess
			created_swipe.save()
			if(created_swipe.swipe_type == "OUT"):
				sess.duration = sess.session_duration()
				sess.save()
				print("session finished")
