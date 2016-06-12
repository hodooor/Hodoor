from django.contrib.staticfiles.testing import StaticLiveServerTestCase, LiveServerTestCase
from selenium import webdriver
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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
from selenium.webdriver.support.wait import WebDriverWait
from attendance.factories import UserFactory, SwipeFactory
from django.contrib.auth.hashers import check_password
from selenium.common.exceptions import NoSuchElementException


#firefox_capabilities = DesiredCapabilities.FIREFOX
#firefox_capabilities['marionette'] = True
#firefox_capabilities['binary'] = '/home/ondra/Documents/'


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

def login_by_form(usr, pswd, webdriver):
	username = webdriver.find_element_by_id("id_username")
	password = webdriver.find_element_by_id("id_password")

	username.send_keys(usr)
	password.send_keys(pswd)

	webdriver.find_element_by_css_selector("input[value='login']").click()

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

		self.assertIn('Hodoor', self.browser.title)

		header_text = self.browser.find_element_by_tag_name('p').text
		self.assertIn("login", header_text)

	def test_login_and_logut_users(self):
		
		user = UserFactory.create(
			first_name = "Ondřej", 
			last_name= "Vičar", 
			password = "admin1324"
		)
		check_password("admin1324", user.password)
		self.browser.get(self.server_url)

		
		login_by_form(user.username,"admin1324", self.browser)

		sessions_header = self.browser.find_element_by_tag_name("h1").text
	
		self.assertIn("Profile", sessions_header)
		self.assertEqual(self.server_url + "/user/" + user.username+ "/",self.browser.current_url)
		self.browser.find_element_by_class_name('a-logout').click()
		self.assertIn(self.server_url + "/login/",self.browser.current_url)
		

	def test_admin_layout_and_styling(self):
		self.browser.get(self.server_url+"/admin/")
		self.browser.set_window_size(1024, 768)

		color = self.browser.find_element_by_id("header").value_of_css_property('background-color')

		self.assertEqual(color, "rgba(65, 118, 144, 1)")

	def test_click_on_logo_returns_home_page(self):

		user = UserFactory.create()

		#logged out - just refreshing page
		self.browser.get(self.server_url)
		self.browser.find_element_by_class_name('navbar-brand').click()
		self.assertEqual(
			self.server_url + "/login/?next=/",
			self.browser.current_url
		)

		#login - logo taking us to profile page
		login_by_form(user.username,"password", self.browser)
		self.assertEqual(
			self.server_url + "/user/" + user.username + "/",
			self.browser.current_url
		)
		self.browser.find_element_by_class_name('navbar-brand').click()
		self.assertEqual(
			self.server_url + "/user/" + user.username + "/",
			self.browser.current_url
		)
		self.browser.find_element_by_class_name('a-logout').click()	
		self.assertIn(self.server_url + "/login/",self.browser.current_url)

	def test_click_on_logout(self):

		user = UserFactory.create()		
		login_by_form(user.username,"password", self.browser)
		self.assertEqual(
			self.server_url + "/user/" + user.username + "/",
			self.browser.current_url
		)
		self.browser.find_element_by_class_name('a-logout').click()
		self.assertIn(self.server_url + "/login/",self.browser.current_url)


	def test_click_on_sessions(self):
		user = UserFactory.create()		
		login_by_form(user.username,"password", self.browser)
		self.browser.find_element_by_class_name('a-sessions').click()
		
		self.assertIn(
			self.server_url + "/sessions/" + user.username + "/",
			self.browser.current_url
		)
		self.browser.find_element_by_class_name('a-logout').click()
		self.assertIn(self.server_url + "/login/",self.browser.current_url)

	def test_click_on_swipes(self):
		user = UserFactory.create()
			
		login_by_form(user.username,"password", self.browser)
		self.browser.find_element_by_class_name('a-swipes').click()
		
		self.assertEqual(
			self.server_url + "/swipes/" + user.username + "/",
			self.browser.current_url
		)
		self.browser.find_element_by_class_name('a-logout').click()
		self.assertIn(self.server_url + "/login/",self.browser.current_url)

	def test_user_cant_access_another_profile(self):
		user1 = UserFactory.create()
		user2 = UserFactory.create()
		login_by_form(user1.username,"password", self.browser)
		self.browser.get(self.server_url + "/sessions/" + user2.username + "/")
		self.assertIn("Restricted", self.browser.page_source, 1)
		self.browser.get(self.server_url + "/swipes/" + user2.username + "/")
		self.assertIn("Restricted", self.browser.page_source, 2)
		self.browser.get(self.server_url + "/user/" + user2.username + "/")
		self.assertIn("Restricted", self.browser.page_source, 3)			
		self.browser.get(self.server_url + "/logout/")
		self.assertIn(self.server_url + "/login/",self.browser.current_url)

	def test_admin_can_access_another_profile(self):
		user1 = UserFactory.create(
			first_name = "Fratišek", 
			last_name= "Vičar", 
			is_staff = True,
		)
		user2 = UserFactory.create()
		self.browser.get(self.server_url)
		login_by_form(user1.username,"password", self.browser)
		self.browser.get(self.server_url + "/user/" + user2.username + "/")
		self.assertIn("Hours", self.browser.page_source)

	def test_there_should_be_no_session_long_time_ago(self):
		
		user = UserFactory.create()
		swipe = SwipeFactory(user = user, swipe_type = "IN")
		login_by_form(user.username,"password", self.browser)
		
		SESSION_URL = self.server_url + "/sessions/" + user.username + "/2014/06/"
		
		self.browser.get(SESSION_URL)
		self.assertEqual(SESSION_URL,self.browser.current_url)
		try:
			element = self.browser.find_element_by_link_text("Detail")
		except NoSuchElementException:
			pass
		else:
			self.fail("There are sessions!")
		finally:
			self.browser.get(self.server_url + "/logout/")
			self.assertIn(self.server_url + "/login/",self.browser.current_url)

class APITestCase(StaticLiveServerTestCase):
	'''
	Testing API for posting and receiving swipes - for clients
	'''
	def setUp(self):
		self.user = UserFactory.create()
		self.token = Token.objects.create(user=self.user)
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

	def test_keys_are_available(self):
		response = self.client.get("/api/keys/")
		self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

	def test_swipes_are_available(self):
		response = self.client.get("/api/swipes/")
		self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

	def test_swipe_can_be_posted(self):
		data = {"user": self.user.id, "swipe_type": "IN", "datetime":"2016-06-04T13:40Z"}
		response = self.client.post("/api/swipes/",data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)