from django.core.urlresolvers import resolve
from django.test import TestCase
from attendance.views import home_page

class HomePageTest(TestCase):

	def test_root_url_resolvers_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
