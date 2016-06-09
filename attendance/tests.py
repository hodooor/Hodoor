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
	Tests isolated Sessions
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
			datetime = timezone.now() + timedelta(hours=50),
			swipe_type = "IN")
		original_session = s1.session
		self.assertTrue(s1.session)
		s2 = Swipe.objects.create(user = User.objects.get(id= 1),
			datetime = timezone.now() + timedelta(hours=60),
			swipe_type = "IN",
			correction_of_swipe = s1)

		self.assertEqual(original_session.swipe_set.filter(swipe_type = "IN").count(), 1)
		
	def test_only_one_in_swipe_in_closed_session(self):
		session = Session.objects.get(id = 1)
		self.create_swipe_new_swipe_with_time_offset(session,50,"IN")
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
	
	def test_get_date(self):
		session = Session.objects.get(id = 1)
		swipe = Swipe.objects.get(id = 1)

		self.assertEqual(swipe.swipe_type, "IN")
		self.assertEqual(session, swipe.session)
		self.assertEqual("<class 'datetime.datetime'>", str(type(session.get_date())))
		self.assertEqual(session.get_date(), swipe.datetime)

class SwipeTestCase(TestCase):
	def setUp(self):
		
		self.USERS = USERS
		self.SWIPES = SWIPES
		self.SWIPE_TYPES = SWIPE_TYPES

		dict_to_database(UserSerializer,self.USERS)
		dict_to_database(SwipeSerializer,self.SWIPES)

	def test_swipes_cant_break_time_integrity(self):
		s1 = Swipe.objects.create(
				id = 100,
				user = User.objects.get(id= 1),
				datetime = timezone.now() + timedelta(hours=150),
				swipe_type = "IN"
			)
		self.assertTrue(Swipe.objects.all().filter(id = 100))
		try:
			s2 = Swipe.objects.create(
				id = 101,
				user = User.objects.get(id= 1),
				datetime = timezone.now() + timedelta(hours=149),
				swipe_type = "OUT"
			)
			self.fail("We cant write new swipe with less datetime")
		except ValueError:
			pass

		self.assertTrue(Swipe.objects.all().filter(id = 100))
		self.assertFalse(Swipe.objects.all().filter(id = 101))

	def test_allowed_types_returns_tupple(self):
		in_return = Swipe.objects.filter(swipe_type = "IN")[0].get_next_allowed_types()
		self.assertIn("tuple", str(type(in_return)))
		in_return = Swipe.objects.filter(swipe_type = "OUT")[0].get_next_allowed_types()
		self.assertIn("tuple", str(type(in_return)))

	def test_cant_break_swipes_integrity(self):
		"""
		Only some sequences of swipes are allowed (IN after IN is not allowed 
		and so on)
		"""
		def create_swipe(type, offset, id):
			return Swipe.objects.create(
				id = id,
				user = User.objects.get(id= 1),
				datetime = timezone.now() + timedelta(hours=offset),
				swipe_type = type
			)
		#we are testing swipes if every last swipe in tupple exists
		SWIPE_SEQUENCE = [
			("IN","IN",),
			("OBR", "OBR",),
			("FBR", "FBR",),
			("OTR", "OTR",),
			("FTR", "FTR",),
			("OUT", "OUT",),
			("FTR",),
			("FBR",),
			("IN","FTR",),
			("FBR",),
		]
		
		offset, id = 50, 50
		
		for tuple_assert in SWIPE_SEQUENCE:
			try:
				for swipe_type in tuple_assert:
					create_swipe(swipe_type, offset, id)
					offset, id = offset + 1, id + 1
				self.fail("It should be imposible to write this swipe_type")
			except ValueError:
					pass
			self.assertFalse(Swipe.objects.all().filter(id = id))