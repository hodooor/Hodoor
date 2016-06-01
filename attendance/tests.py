from django.core.urlresolvers import resolve
from django.test import TestCase
from attendance.views import home_page
from django.contrib.auth.models import User

from django.http import HttpRequest
from .models import Session, Swipe
from const_data import generate_random_datetimes_for_swipes
from .serializers import SwipeSerializer, UserSerializer
from const_data import USERS, SWIPES, SWIPE_TYPES
from datetime import datetime, timedelta
from django.utils import timezone

def dict_to_database(serializer_class, list_of_dict):
	'''
	Input is serializer class type object and list of dictionaries
	save to database
	'''
	for diction in list_of_dict:
		ser = serializer_class(data = diction)
		ser.is_valid()
		ser.save()

class SessionTestCase(TestCase):
	'''
	Tests isolated Sessions and Swipes
	'''
	def setUp(self):
		
		self.USERS = USERS
		self.SWIPES = SWIPES
		self.SWIPE_TYPES = SWIPE_TYPES

		dict_to_database(UserSerializer,self.USERS)
		dict_to_database(SwipeSerializer,self.SWIPES)

	def test_session_duration_methods(self):
		for session in Session.objects.all():
			self.assertEqual(
				session.session_duration(),
				session.session_duration_overall() - session.breaks_duration()
			)
	def test_number_of_breaks_method(self):
		for session in Session.objects.all():
			self.assertEqual(
				session.num_of_breaks(),
				self.SWIPE_TYPES.count("FBR")
			)
	def test_only_one_in_swipe_in_opened_session(self):
		s1 = Swipe.objects.create(user = User.objects.get(id= 1),
			datetime = timezone.now() + timedelta(hours=1),
			swipe_type = "IN")
		original_session = s1.session
		self.assertTrue(s1.session)

		s2 = Swipe.objects.create(user = User.objects.get(id= 1),
			datetime = timezone.now() + timedelta(hours=2),
			swipe_type = "IN",
			correction_of_swipe = s1)

		self.assertEqual(original_session.swipe_set.filter(swipe_type = "IN").count(), 1)

		
	def test_only_one_in_swipe_in_closed_session(self):
		session = Session.objects.get(id = 1)
		original_in_swipe = session.swipe_set.get(swipe_type = "IN")

		new_in_swipe = Swipe.objects.create(
			user = User.objects.get(id = original_in_swipe.id),
			datetime = original_in_swipe.datetime - timedelta(hours=1),
			swipe_type = "IN",
			correction_of_swipe = original_in_swipe)
		self.assertEqual(session.swipe_set.filter(swipe_type = "IN").count(), 1)
