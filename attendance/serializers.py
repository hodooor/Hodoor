from .models import Swipe
from rest_framework import serializers
from django.contrib.auth.models import User

class SwipeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Swipe
		fields = ('datetime', 'swipe_type') #should add users