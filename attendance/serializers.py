from .models import Swipe,Key
from rest_framework import serializers
from django.contrib.auth.models import User

class SwipeSerializer(serializers.ModelSerializer):
	'''
	Serializer for sending swipes.. Hyperlink serializer does not work with user foreign key
	'''
	class Meta:
		model = Swipe
		fields = ('user','datetime', 'swipe_type','id') #should add users

class UserSerializer(serializers.ModelSerializer):
	'''
	Serializer used for prepopulating database and geting key information by client
	'''
	class Meta:
		model = User
		fields = ('username','id')

class KeySerializer(serializers.ModelSerializer):
	'''
	Including user information for client
	'''
	user = UserSerializer(read_only = True)
	class Meta:
		model = Key
		fields = ('user','id', 'key_type')