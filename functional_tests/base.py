import sys
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerCase
from django.conf import settings

from .server_tools import reset_database
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

SCREEN_DUMP_LOCATION = os.path.abspath(
		os.path.join(os.path.dirname(__file__), 'screendump')
)


class FunctionalTest(StaticLiveServerCase): 
	# instead of <unittest.TestCase>
	
	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_host = arg.split('=')[1]
				cls.server_url = 'http://' + cls.server_host
				cls.against_staging = True
				return 
		super().setUpClass()
		cls.against_staging = False
		cls.server_url = cls.live_server_url
	
	@classmethod
	def tearDownClass(cls):
		if not cls.against_staging:
			super().tearDownClass()

	def setUp(self):
		if self.against_staging:
			reset_database(self.server_host)
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3) # it won't work on every case
	
	def tearDown(self):
		# to get a screenshot
		if not self._outcomeForDoCleanups.success:
			if not os.path.exists(SCREEN_DUMP_LOCATION):
				os.makedirs(SCREEN_DUMP_LOCATION)
			for ix, handle in enumerate(self.browser.window_handles):
				self._windowid = ix
				self.browser.switch_to_window(handle)
				self.take_screenshot()
				self.dump_html()
		self.browser.quit()
		super().tearDown()
	
	# helper method
	def take_screenshot(self):
		filename = self._get_filename() + '.png'
		print('screenshotting to ', filename)
		self.browser.get_screenshot_as_file(filename)
	
	def dump_html(self):
		filename = self._get_filename() + '.html'
		print('dumping page HTML to ', filename)
		with open(filename, 'w') as f:
			f.write(self.browser.page_source)
	
	def _get_filename(self):
		timestamp = datetime.now().isoformat().replace(':', '')
		return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
				folder=SCREEN_DUMP_LOCATION,
				classname=self.__class__.__name__,
				method=self._testMethodName,
				windowid=self._windowid,
				timestamp=timestamp
		)


	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows] )

	def get_item_input_box(self):
		return self.browser.find_element_by_id('id_text')


	# using selenuim WebDriverWait for 'explicit wait'
	def wait_for_element_with_id(self, element_id):
		WebDriverWait(self.browser, timeout=30).until(
				lambda b: b.find_element_by_id(element_id),
				'Could not find element with if {}. Page text was was {}'.format(
					element_id, self.browser.find_element_by_tag_name('body').text
				)
		)

	# helper
	def wait_to_be_logged_in(self, email):
		self.wait_for_element_with_id('id_logout')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn(email, navbar.text)
	
	def wait_to_be_logged_out(self, email):
		self.wait_for_element_with_id('id_login')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertNotIn(email, navbar.text)
	
	def create_pre_authenticated_session(self, email):
		if self.against_staging:
			session_key = create_session_on_server(self.server_host, email)
		else:
			session_key = create_pre_authenticated_session(email)
				
		## to set a cookie we neer to first visit the domain.
		## 404 pages load the quickest!
		self.browser.get(self.server_url + "/404_no_such_url/")
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session_key,
			path='/',
		))
	

