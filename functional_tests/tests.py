from django.test import LiveServerTestCase
from selenium import webdriver
from const_data import USERS, SWIPES, SWIPE_TYPES
from attendance.tests import dict_to_database
from attendance.serializers import UserSerializer, SwipeSerializer
from django.contrib.auth.models import User
from django.conf import settings

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		#Prepopulate database with test data
		if settings.DEBUG == False:
			settings.DEBUG = True

		self.USERS = USERS
		self.SWIPES = SWIPES
		self.SWIPE_TYPES = SWIPE_TYPES
		self.TEST_PASSWORD = "user1234"

		dict_to_database(UserSerializer,self.USERS)
		dict_to_database(SwipeSerializer,self.SWIPES)

		users = User.objects.all()
		
		for user in users:
			user.set_password(self.TEST_PASSWORD)
			user.save()

		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_home_page_login(self):
		
		self.browser.get(self.live_server_url)

		#page title is ticker
		self.assertIn('Ticker', self.browser.title)

		#ẅe should see login page
		header_text = self.browser.find_element_by_tag_name('p').text
		self.assertIn("login", header_text)

		username = self.browser.find_element_by_id("id_username")
		password = self.browser.find_element_by_id("id_password")

		username.send_keys(self.USERS[0]["username"])
		password.send_keys(self.TEST_PASSWORD)
		self.browser.find_element_by_css_selector("input[value='login']").click()

		sessions_header = self.browser.find_element_by_tag_name("h1").text
		self.assertIn("Sessions", sessions_header)
