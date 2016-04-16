from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Session(models.Model):
	'''
	Session is from login swipe to logout swipe and can have one or 
	more breaks
	'''

	user = models.ForeignKey(User)
	duration = models.DurationField(null = True)

	description = models.CharField(max_length = 100, null = True) 
	modified = models.BooleanField(default = False) 

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
					("FBR","From Break")		
	)

	user = models.ForeignKey(User)
	datetime = models.DateTimeField("Datetime of swipe")

	swipe_type = models.CharField(max_length=3, choices = SWIPE_TYPES)

	session = models.ForeignKey(Session,null = True, blank = True)
	def __str__(self):
		return str(self.id) + " " + self.user.username + " " + self.swipe_type



@receiver(post_save, sender = Swipe)
def post_process_swipes(sender=Swipe, **kwargs):
	if(kwargs['created']): # trigering only when swipe was created
		
		#swipe object that was just created
		created_swipe = kwargs["instance"] 

		if(created_swipe.swipe_type == "IN"):
			
			#session has same user as swipe
			sess = Session(user = created_swipe.user)
			sess.save()

			#swipe is related to session 
			created_swipe.session = sess
			created_swipe.save()
			
		elif(kwargs["instance"].swipe_type == "OBR"):
			#s = Session.objects.get(user = kwargs["instance"].user)
			print("YES")

		elif(kwargs["instance"].swipe_type == "FBR"):
			print("FBR")
		elif(kwargs["instance"].swipe_type == "OUT"):
			print("OUT")