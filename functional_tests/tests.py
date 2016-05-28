from django.test import LiveServerTestCase
from selenium import webdriver
from const_data import USERS, SWIPES, SWIPE_TYPES
from attendance.tests import dict_to_database
from attendance.serializers import UserSerializer, SwipeSerializer
from django.contrib.auth.models import User
from django.conf import settings

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

class NewVisitorTest(LiveServerTestCase):
		#Prepopulate database with test data


	def setUp(self):

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


	def test_login_and_logut_users(self):
		populate_database(self)

		for user in self.USERS:
			self.browser.get(self.live_server_url)
			username = self.browser.find_element_by_id("id_username")
			password = self.browser.find_element_by_id("id_password")
			
			username.send_keys(user["username"])
			password.send_keys(self.TEST_PASSWORD)
			self.browser.find_element_by_css_selector("input[value='login']").click()

			sessions_header = self.browser.find_element_by_tag_name("h1").text
			self.assertIn("Sessions", sessions_header)

			self.browser.get(self.live_server_url+ "/logout/")
