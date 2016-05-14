from .models import Swipe,Key, UserMethods
from rest_framework import serializers
from django.contrib.auth.models import User

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

	class Meta:
		model = User
		fields = ('username','id','last_swipe')

	def get_last_swipe(self,obj): 
		#if current user has some swipes
		if(Swipe.objects.all().filter(user=obj)):
			serializer = SwipeSerializerLight(obj.swipe_set.latest('datetime'))
			return serializer.data
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
