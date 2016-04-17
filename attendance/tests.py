from django.core.urlresolvers import resolve
from django.test import TestCase
from attendance.views import home_page
from django.contrib.auth.models import User

from django.http import HttpRequest
from .models import Session, Swipe
from django.utils import timezone
from datetime import timedelta
from random import randint
from rest_population import generate_random_datetimes_for_swipes

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
		
		#generate imput data
		USERNAMES = ("ondrej.vicar","lukas.krcma","jaroslav.malec")
		SWIPE_TYPES = ("IN","OBR", "FBR","OBR", "FBR","OUT")
		DATE_TIMES = generate_random_datetimes_for_swipes(SWIPE_TYPES)
		
		self.INPUT_DATA = []

		for user in USERNAMES:
			self.INPUT_DATA.append({
				"username":user,
				"swipe_types":SWIPE_TYPES,
				"datetimes":generate_random_datetimes_for_swipes(SWIPE_TYPES),
			})
		
		print(self.INPUT_DATA)
		#now posting thoes swipes
		for user in self.INPUT_DATA:
			u = User.objects.create(username = user["username"])
	
			for swipe_type, datetime in zip(user["swipe_types"],user["datetimes"]):

				swip = Swipe.objects.create(
					user = u,
					datetime = datetime,
					swipe_type = swipe_type,
				)
		
		print(Session.objects.all())	

	def test_(self):


		self.assertTrue(True)
