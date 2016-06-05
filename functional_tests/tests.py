from django.contrib.staticfiles.testing import StaticLiveServerTestCase, LiveServerTestCase
from selenium import webdriver
from const_data import USERS, SWIPES, SWIPE_TYPES
from attendance.tests import dict_to_database
from attendance.serializers import UserSerializer, SwipeSerializer
from django.contrib.auth.models import User
from django.conf import settings
from attendance.models import Key, Swipe
from selenium.webdriver.support.wait import WebDriverWait
from django.test.utils import override_settings
from django.test import TestCase
from rest_framework import status
import sys
import re
from rest_framework.test import APIClient
from unittest import skip
from rest_framework.authtoken.models import Token

def populate_database(what_pop):
	what_pop.USERS = USERS
	what_pop.SWIPES = SWIPES
	what_pop.SWIPE_TYPES = SWIPE_TYPES
	what_pop.TEST_PASSWORD = "user1234"

	dict_to_database(UserSerializer,what_pop.USERS)
	dict_to_database(SwipeSerializer,what_pop.SWIPES)

	users = User.objects.all()
	
	for user in users:
		user.set_password(what_pop.TEST_PASSWORD)
		user.save()

class NewVisitorTest(StaticLiveServerTestCase):
	
	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				cls.browser = webdriver.Firefox()
				cls.browser.implicitly_wait(3)
				return
		super(NewVisitorTest, cls).setUpClass()
		cls.server_url = cls.live_server_url
		cls.browser = webdriver.Firefox()
		cls.browser.implicitly_wait(3)

	@classmethod
	def tearDownClass(cls):
		cls.browser.close()
		super(NewVisitorTest, cls).tearDownClass()

	def test_home_page_login(self):
		
		self.browser.get(self.server_url)

		#page title is ticker
		self.assertIn('Ticker', self.browser.title)

		#ẅe should see login page
		header_text = self.browser.find_element_by_tag_name('p').text
		self.assertIn("login", header_text)

	def test_login_and_logut_users(self):
		from selenium.webdriver.support.wait import WebDriverWait
		timeout = 2
		populate_database(self) #only local server

		for user in self.USERS[:1]:
			self.browser.get(self.server_url)
			#print(type(self.live_server_url))
			username = self.browser.find_element_by_id("id_username")
			password = self.browser.find_element_by_id("id_password")
			
			username.send_keys(user["username"])
			password.send_keys(self.TEST_PASSWORD)
			
			self.browser.find_element_by_css_selector("input[value='login']").click()
			WebDriverWait(self.browser, timeout).until( lambda driver: driver.find_element_by_tag_name('body'))
			
			sessions_header = self.browser.find_element_by_tag_name("h1").text
			self.assertIn("Profile", sessions_header)
			self.browser.get("%s%s" % (self.server_url, '/logout/'))
			WebDriverWait(self.browser, timeout).until( lambda driver: driver.find_element_by_tag_name('body'))
			self.assertIn('Logged out', self.browser.title)

	def test_admin_layout_and_styling(self):
		self.browser.get(self.server_url+"/admin/")
		self.browser.set_window_size(1024, 768)

		color = self.browser.find_element_by_id("header").value_of_css_property('background-color')

		self.assertEqual(color, "rgba(65, 118, 144, 1)")

	def test_click_on_logo_returns_index_page(self):
		self.browser.get(self.server_url)
		self.browser.find_element_by_class_name('navbar-brand').click()
		self.assertEqual(self.server_url + "/login/?next=/",self.browser.current_url)

	def test_click_on_logout(self):
		self.browser.get(self.server_url)
		self.browser.find_element_by_class_name('a-logout').click()
		self.assertEqual(self.server_url + "/logout/",self.browser.current_url)

class APITestCase(StaticLiveServerTestCase): #works with TestCase or with --reverse flag during tests
	def setUp(self):
		self.user = User.objects.create(username = "ondrej.vicar", password = "user1234")
		self.token = Token.objects.create(user=self.user)
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

	def test_keys_are_available(self):
		response = self.client.get("/keys/")
		self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

	def test_swipes_are_available(self):
		response = self.client.get("/swipes/")
		self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

	def test_swipe_can_be_posted(self):
		data = {"user": self.user.id, "swipe_type": "IN", "datetime":"2016-06-04T13:40Z"}
		response = self.client.post("/swipes/",data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)