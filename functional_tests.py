from selenium import webdriver
import unittest

SERVER_URL = "http://localhost:8000"

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_ticker_in_title(self):
		self.browser.get(SERVER_URL)
		self.assertIn('ticker', self.browser.title)

		self.fail('Finish the test!')

if __name__ == '__main__':
	unittest.main()