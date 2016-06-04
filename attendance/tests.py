from django.core.urlresolvers import resolve
from django.test import TestCase
from attendance.views import home_page
from django.contrib.auth.models import User
from unittest import skip

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


	def create_swipe_new_swipe_with_time_offset(self, session, offset_hours, swipe_type):
		"""
		For testing purposes, returns  new_swipe, original_swipe tupple 
		"""
		original_swipe = session.swipe_set.get(swipe_type = swipe_type)
		new_swipe = Swipe.objects.create(
			user = original_swipe.user,
			datetime = original_swipe.datetime + timedelta(hours=offset_hours),
			swipe_type = swipe_type,
			correction_of_swipe = original_swipe)
		return new_swipe,original_swipe

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
		self.create_swipe_new_swipe_with_time_offset(session,1.5,"IN")	
		self.assertEqual(session.swipe_set.filter(swipe_type = "IN").count(), 1)

	def test_only_one_swipe_out_closed_session(self):
		session = Session.objects.get(id = 2)
		self.create_swipe_new_swipe_with_time_offset(session,-1,"OUT")		
		self.assertEqual(session.swipe_set.filter(swipe_type = "OUT").count(), 1)
	
	def test_session_duration_is_recalculated_for_correcting_swipe(self):
		session = Session.objects.get(id = 1)
		self.create_swipe_new_swipe_with_time_offset(session,-1,"OUT")
		self.assertEqual(session.duration, session.session_duration())

	def test_is_at_work(self):
		pass
	
	def test_session_swipes_cant_break_time_integrity(self):
		pass

	def test_cant_break_swipes_integrity(self):
		def create_swipe(type, offset, id):
			return Swipe.objects.create(
				id = id,
				user = User.objects.get(id= 1),
				datetime = timezone.now() + timedelta(hours=offset),
				swipe_type = type
			)
		

		create_swipe("IN", 1, 50)
		create_swipe("IN", 2, 51)
		
		create_swipe("OBR", 3, 52)
		create_swipe("OBR", 4, 53)
		
		create_swipe("FBR", 5, 54)
		create_swipe("FBR", 6, 55)
		
		create_swipe("OTR", 7, 56)
		create_swipe("OTR", 8, 57)
		
		create_swipe("FTR", 9, 58)
		create_swipe("FTR", 10, 59)
		
		create_swipe("OUT",11, 60)
		create_swipe("OUT",12, 61)

		self.assertTrue(Swipe.objects.all().filter(id = 50))
		self.assertFalse(Swipe.objects.all().filter(id = 51))
		self.assertFalse(Swipe.objects.all().filter(id = 53))
		self.assertFalse(Swipe.objects.all().filter(id = 55))
		self.assertFalse(Swipe.objects.all().filter(id = 57))
		self.assertFalse(Swipe.objects.all().filter(id = 59))
		self.assertFalse(Swipe.objects.all().filter(id = 61))

	def test_allowed_types_returns_tupple(self):
		in_return = Swipe.objects.filter(swipe_type = "IN")[0].get_next_allowed_types()
		self.assertIn("tuple", str(type(in_return)))
		in_return = Swipe.objects.filter(swipe_type = "OUT")[0].get_next_allowed_types()
		self.assertIn("tuple", str(type(in_return)))