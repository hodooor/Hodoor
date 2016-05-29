from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from const_data import USERS, SWIPES, SWIPE_TYPES
from attendance.tests import dict_to_database
from attendance.serializers import UserSerializer, SwipeSerializer
from django.contrib.auth.models import User
from django.conf import settings
from selenium.webdriver.support.wait import WebDriverWait
from django.test.utils import override_settings
from django.conf import settings
from django.test import TestCase

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

class NewVisitorTest(StaticLiveServerTestCase, TestCase):
	
	@classmethod
	def setUpTestData(cls):
		
		cls.USERS = USERS
		cls.SWIPES = SWIPES
		cls.SWIPE_TYPES = SWIPE_TYPES
		cls.TEST_PASSWORD = "user1234"

		dict_to_database(UserSerializer,cls.USERS)
		dict_to_database(SwipeSerializer,cls.SWIPES)

		users = User.objects.all()
	
		for user in users:
			user.set_password(cls.TEST_PASSWORD)
			print(cls.TEST_PASSWORD)
			user.save()
		print(users)
		super().setUpTestData()
	
	def setUp(self):

		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.close()

	def test_home_page_login(self):
		
		self.browser.get(self.live_server_url)

		#page title is ticker
		self.assertIn('Ticker', self.browser.title)

		#ẅe should see login page
		header_text = self.browser.find_element_by_tag_name('p').text
		self.assertIn("login", header_text)

	def test_login_and_logut_users(self):
		from selenium.webdriver.support.wait import WebDriverWait
		timeout = 2
		#populate_database(self)
		for user in self.USERS:
			self.browser.get(self.live_server_url)
			#print(type(self.live_server_url))
			username = self.browser.find_element_by_id("id_username")
			password = self.browser.find_element_by_id("id_password")
			
			username.send_keys(user["username"])
			password.send_keys(self.TEST_PASSWORD)
			
			self.browser.find_element_by_css_selector("input[value='login']").click()
			WebDriverWait(self.browser, timeout).until( lambda driver: driver.find_element_by_tag_name('body'))
			
			sessions_header = self.browser.find_element_by_tag_name("h1").text
			self.assertIn("Sessions", sessions_header)
			self.browser.get("%s%s" % (self.live_server_url, '/logout/'))
			#WebDriverWait(self.browser, timeout).until( lambda driver: driver.find_element_by_tag_name('body'))
			#self.browser.implicitly_wait(3)
			#self.assertIn('Logged out', self.browser.title)