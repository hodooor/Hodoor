from .models import Swipe,Key, Session
from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Sum

class SwipeSerializer(serializers.ModelSerializer):
	'''
	Serializer for recieving swipes from client.. Hyperlink serializer does not work with user foreign key
	'''
	class Meta:
		model = Swipe
		fields = ('user','datetime', 'swipe_type','id') #should add users

class SwipeSerializerLight(serializers.ModelSerializer):
	'''
	Serializer for  swipes.. Light version without user information
	'''
	class Meta:
		model = Swipe
		fields = ('datetime', 'swipe_type','id') #should add users

class UserSerializer(serializers.ModelSerializer):
	'''
	Serializer used for prepopulating database and geting key information by client
	'''
	last_swipe = serializers.SerializerMethodField()
	hours_this_month = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ('username','id','last_swipe', 'hours_this_month')

	def get_last_swipe(self,obj): 
		#if current user has some swipes
		if(Swipe.objects.all().filter(user=obj)):
			serializer = SwipeSerializerLight(obj.swipe_set.latest('datetime'))
			return serializer.data
		else:
			return 0
	def get_hours_this_month(self,obj):
		#all in swipes for current user this month
		swipes = Swipe.objects.filter(swipe_type="IN", user=obj, datetime__month=datetime.now().month)
		if swipes:
			swipes = swipes.values_list('id', flat=True)
		
			sessions = Session.objects.filter(swipe__in = swipes) #why not swipe_set??
			duration_seconds = sessions.aggregate(Sum('duration'))["duration__sum"]
			if(duration_seconds):
				duration_seconds = duration_seconds.total_seconds()
			else:
				return 0
			return duration_seconds/3600 #hours
		else:
			return 0


class KeySerializer(serializers.ModelSerializer):
	'''
	Including user information for client
	'''
	user = UserSerializer(read_only = True)
	class Meta:
		model = Key
		fields = ('user','id', 'key_type')
