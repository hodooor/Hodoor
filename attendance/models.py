from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Q
from datetime import datetime, timezone, timedelta
from django.db.models import Sum

class SessionManager(models.Manager):
	def get_sessions_this_month(self):
		"""
		returns List of sessions made this month
		"""
		swipes_this_month = Swipe.objects.filter(swipe_type="IN", datetime__month=datetime.now().month)
		if swipes_this_month:
			swipes_list = swipes_this_month.values_list('id', flat=True)
			sessions = Session.objects.filter(swipe__in = swipes_list) #why not swipe_set??
			return sessions
		else:
			return 0

	def get_hours_this_month(self, user):
		"""
		Returns number of hours for given user id this month
		"""
		sessions_this_month = self.get_sessions_this_month()
		if(sessions_this_month):
			sessions = sessions_this_month.filter(user=user)
			new_dur = timedelta(0)
			for session in sessions:
				new_dur += session.session_duration()
			return new_dur.total_seconds()/3600
		else:
			return 0	
class Project(models.Model):
	name = models.CharField(max_length = 20)

	#so we can define private projects (hours in this project does not count)
	private = models.BooleanField(default = False)
	description = models.CharField(
		max_length = 100, 
		null = True, 
		blank = True
	)
	#maybe worked hours? or will be calculated dynamicaly?
	
	def __str__(self):
		return self.name

class Session(models.Model):
	'''
	Session is from login swipe to logout swipe and can have one or 
	more breaks
	'''

	user = models.ForeignKey(User)
	#this is saved field and exists only for finished sessions
	duration = models.DurationField(null = True, blank = True)

	modified = models.BooleanField(default = False)
	
	project = models.ManyToManyField(Project, through = "ProjectSeparation")

	objects = SessionManager() 
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
		duration = timedelta(0)

		for obr_object, fbr_object  in zip(obr,fbr):
			duration += fbr_object.datetime - obr_object.datetime

		if len(obr) > len(fbr): #if we are on break
			duration += datetime.now(timezone.utc) - obr.latest("datetime").datetime
	
		return duration
			
	def session_duration_overall (self):
		'''
		Returns time delta duration of session(including breaks)
		'''

		login_datetime = self.swipe_set.get(swipe_type = "IN").datetime
		
		if(self.is_session_complete()):
			end_datetime = self.swipe_set.get(swipe_type = "OUT").datetime
		else:
			end_datetime = datetime.now(timezone.utc)
		return end_datetime - login_datetime

	def session_duration(self):
		'''
		Returns time delta duration of session(excluding breaks)
		'''

		return self.session_duration_overall() - self.breaks_duration()

	def is_session_complete(self):
		if(self.swipe_set.filter(swipe_type = "OUT").exists()):
			return True
		else:
			return False

	def __str__(self):
		return str(self.id) + " " + str(self.user)

class ProjectSeparation(models.Model):
	'''
	So we can time divide our session into more projects
	'''
	session = models.ForeignKey(Session)
	project = models.ForeignKey(Project)

	#this describes the activity
	description = models.CharField(
		max_length = 100, 
		null = True, 
		blank = True
	)
	#maybe entered in percentages
	time_spend = models.DurationField() 

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

	#session should be specified for correcting swipe
	session = models.ForeignKey(Session,
		null = True, 
		blank = True, 
		on_delete = models.SET_NULL,
		)
	source = models.CharField(max_length = 5,null = True, blank = True)

	#this points to swipe that is correction of this one
	correction_of_swipe = models.ForeignKey(
		"self",
		on_delete=models.CASCADE,
		blank = True,
		null = True, #if blank, this swipe is the right one 
		)
	def get_next_allowed_types(self):
		"""
		Returns tupple of types that can be used in next swipe
		"""
		if self.swipe_type == "IN":
			return "OBR", "OTR","OUT",
		elif self.swipe_type == "OUT":
			return "IN",
		elif self.swipe_type == "OBR":
			return "FBR",
		elif self.swipe_type == "FBR":
			return "OBR", "OTR","OUT",
		elif self.swipe_type == "OTR":
			return "FTR",
		elif self.swipe_type == "FTR": 
			return "OBR", "OTR","OUT",
		else:
			return "0"

	def __str__(self):
		return str(self.id) + " " + self.user.username + " " + self.swipe_type

	def save(self, *args, **kwargs):
		if(self._state.adding and not self.correction_of_swipe):
			try:
				latest_swipe = Swipe.objects.filter(user = self.user).order_by("-pk")[0]


				if self.swipe_type not in latest_swipe.get_next_allowed_types():
					raise ValueError("Wrong swipe_type field")
					return

				if self.datetime < latest_swipe.datetime:
					raise ValueError("Wrong datetime field")
					return

			except IndexError:
				#we have no records for given user, this is probably faster than "if"
				pass

		super(Swipe, self).save(*args, **kwargs)


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
	if kwargs['created']: # trigering only when swipe was created
		
		#swipe object that was just created
		created_swipe = kwargs["instance"]		
		
		if created_swipe.correction_of_swipe: 

			orig_swipe = Swipe.objects.get(id = created_swipe.correction_of_swipe.id)
			orig_swipe.session = None;
			orig_swipe.save()

			created_swipe.session = created_swipe.correction_of_swipe.session
			created_swipe.save()
			
			created_swipe.session.duration = created_swipe.session.session_duration()
			created_swipe.session.save()


		#open new session if created swipe is not correction of old one 
		else:
			if created_swipe.swipe_type == "IN":
				sess = Session(user = created_swipe.user)
				sess.save()

				#swipe is related to session 
				created_swipe.session = sess
				created_swipe.save()

			#updated oppened session
			else:

				sess = Session.objects.filter(user = created_swipe.user)

				#session without OUT swipe (open session)
				sess = sess.exclude(swipe__swipe_type = "OUT")
				if len(sess) == 1:
					sess = sess[0]
				else:
					raise ValueError('More Opened Sessions')
						
				created_swipe.session = sess
				created_swipe.save()
				if created_swipe.swipe_type == "OUT":
					sess.duration = sess.session_duration()
					sess.save()

