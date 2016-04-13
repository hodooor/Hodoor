from .models import Swipe
from rest_framework import serializers
from django.contrib.auth.models import User

class SwipeSerializer(serializers.ModelSerializer):
	'''
	Serializer for sending swipes.. Hyperlink serializer does not work with user foreign key
	'''
	class Meta:
		model = Swipe
		fields = ('user','datetime', 'swipe_type','id') #should add users
