from django.core.urlresolvers import resolve
from django.test import TestCase
from attendance.views import home_page
from django.contrib.auth.models import User

from django.http import HttpRequest
from .models import Session, Swipe
from django.utils import timezone
from datetime import timedelta
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
		SWIPE_TYPES = ["IN","OBR", "FBR","OBR", "FBR","OUT"]
		DATETIMES = []
		
		t = timezone.now()

		hours_increment = 4

		for swipe in SWIPE_TYPES:
			DATETIMES.append(
				(t + timedelta(hours = hours_increment)).isoformat()
				)
			hours_increment += 4

		print(SWIPE_TYPES)
		print(DATETIMES)

		u = User.objects.create(username = "ondrej.vicar")
		swip = Swipe.objects.create(
			user = u, 
			datetime= timezone.now(),
			swipe_type = "IN" 
			)
		print(swip,Session.objects.all())	

	def test_(self):


		self.assertTrue(True)