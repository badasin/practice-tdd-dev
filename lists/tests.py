# base
from django.test import TestCase
# addition
from django.core.urlresolvers import resolve
from lists.views import home_page

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		# function called home_page
		self.assertEqual(found.func, home_page)


'''
# checking it works
# Create your tests here.

class SmokeTest(TestCase):

	def test_bad_maths(self):
		self.assertEqual(1+1, 3)
'''
