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
	Tests isolated Sessions
	'''
	def setUp(self):
		
		#generate imput data
		USERNAMES = ["ondrej.vicar","lukas.krcma","jaroslav malec"]
		SWIPE_TYPES = ["IN","OBR", "FBR","OBR", "FBR","OUT"]
	
		#now posting thoes swipes
		for username_ in USERNAMES:
			u = User.objects.create(username = username_)
			datetimes = generate_random_datetimes_for_swipes(SWIPE_TYPES)

			for s_t, dt in zip(SWIPE_TYPES, datetimes):

				swip = Swipe.objects.create(
					user = u,
					datetime = dt,
					swipe_type = s_t,
				)
		
		print(Session.objects.all())	

	def test_(self):


		self.assertTrue(True)
