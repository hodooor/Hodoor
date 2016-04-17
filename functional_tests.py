from selenium import webdriver
from django.unittest import TestCase

SERVER_URL = "http://localhost:8000"

class NewVisitorTest(TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_home_page_full_of_swipes_with_heaer(self):
		self.browser.get(SERVER_URL)

		#page title is ticker
		self.assertIn('ticker', self.browser.title)

		#header text on page containts Swipes - page should be swipes table
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn("Swipes", header_text)

		self.fail('Finish the test!')

	#page /attendance/user/sessions/ - should be table with sessions for logged in user

	#page /attendance/user/sessions/1 - should be detailed editable form session

	#page /attendance/api/ this url should be for post request with swipes

	#models.. there will redefined user profiles,
			#and sessions  should have foreigh key also users and should be completed after logout
			#and swipes.. swipes should have forgeinkez sessions and user and should be instantly assigned 
			#after post request tru api

			#maybe use django.db.models.signals.post_save




if __name__ == '__main__':
	unittest.main()