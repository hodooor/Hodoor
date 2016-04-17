from django.core.urlresolvers import resolve
from django.test import TestCase
from attendance.views import home_page
from django.contrib.auth.models import User

from django.http import HttpRequest
from .models import Session, Swipe
from rest_population import generate_random_datetimes_for_swipes
from .serializers import SwipeSerializer, UserSerializer

def dict_to_database(serializer_class, list_of_dict):
	'''
	Input is serializer class type object and list of dictionaries
	save to database
	'''
	print(type(serializer_class), type(list_of_dict))
	for diction in list_of_dict:
		ser = serializer_class(data = diction)
		ser.is_valid()
		ser.save()


class HomePageTest(TestCase):

	def test_root_url_resolvers_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		self.assertTrue(response.content.startswith(b'<html>'))
		self.assertIn(b'<title>ticker</title>', response.content)
		self.assertIn(b'<h1>', response.content)
		self.assertTrue(response.content.endswith(b'</html>'))

class SessionTestCase(TestCase):
	'''
	Tests isolated Sessions and Swipes
	'''
	def setUp(self):
		
		
		self.USERS = [
			{"username":"ondrej.vicar", "id":"1"},
			{"username":"jaroslav.malec", "id":"2"},
			{"username":"lukas.krcma", "id":"3"},
			{"username":"david.binko", "id":"4"},
		]
		self.SWIPE_TYPES = ("IN","OBR", "FBR","OBR", "FBR","OUT")
		#now generate swipe list of dictionaries
		self.SWIPES = []
		for user_id in (d['id'] for d in self.USERS):
			
			datetime = generate_random_datetimes_for_swipes(self.SWIPE_TYPES)
			
			for swipe_type,datetime in zip(self.SWIPE_TYPES,datetime):
				self.SWIPES.append({
					"user":user_id,
					"swipe_type":swipe_type,
					"datetime":datetime,
				})

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



		self.assertTrue(True)
