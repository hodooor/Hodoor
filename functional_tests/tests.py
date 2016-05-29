from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from const_data import USERS, SWIPES, SWIPE_TYPES
from attendance.tests import dict_to_database
from attendance.serializers import UserSerializer, SwipeSerializer
from django.contrib.auth.models import User
from django.conf import settings
from selenium.webdriver.support.wait import WebDriverWait
from django.test.utils import override_settings
from django.test import TestCase
import sys
import re

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
	
	# @classmethod
	# def setUpTestData(cls):
		
	# 	cls.USERS = USERS
	# 	cls.SWIPES = SWIPES
	# 	cls.SWIPE_TYPES = SWIPE_TYPES
	# 	cls.TEST_PASSWORD = "user1234"

	# 	dict_to_database(UserSerializer,cls.USERS)
	# 	dict_to_database(SwipeSerializer,cls.SWIPES)

	# 	users = User.objects.all()
	
	# 	for user in users:
	# 		user.set_password(cls.TEST_PASSWORD)
	# 		print(cls.TEST_PASSWORD)
	# 		user.save()
	# 	print(users)
	# 	super().setUpTestData()
	
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