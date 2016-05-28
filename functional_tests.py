from selenium import webdriver
import unittest

SERVER_URL = "http://10.0.0.200:8000/"

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_home_page_login(self):
		self.browser.get(SERVER_URL)

		#page title is ticker
		self.assertIn('Ticker', self.browser.title)

		#ẅe should see login page
		header_text = self.browser.find_element_by_tag_name('p').text
		self.assertIn("login", header_text)

		username = self.browser.find_element_by_id("id_username")
		password = self.browser.find_element_by_id("id_password")

		username.send_keys("ondrej.vicar")
		password.send_keys("admin1234")
		self.browser.find_element_by_css_selector("input[value='login']").click()

		sessions_header = self.browser.find_element_by_tag_name("h1").text
		self.assertIn("Sessions", sessions_header)
		
if __name__ == '__main__':
	unittest.main()