from .base import FunctionalTest
from selenium.webdriver.support.ui import WebDriverWait
import time

class LoginTest(FunctionalTest):

	def test_login_with_persona(self):
		# sign-in
		self.browser.get(self.server_url)
		self.browser.find_element_by_id('id_login').click()

		self.switch_to_new_window('Mozilla Persona')

		self.browser.find_element_by_id('authentication_email'
				).send_keys('edith@mockmyid.com')
		self.browser.find_element_by_tag_name('button').click()

		self.switch_to_new_window('To-Do')
		self.wait_for_element_with_id('id_logout')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn('edith@mockmyid.com', navbar.text)
		
		# login and logout
		self.switch_to_new_window('To-Do')
		self.wait_to_be_logged_in()
		self.browser.refresh()
		self.wait_to_be_logged_in()
		self.browser.find_element_by_id('id_logout').click()
		self.wait_to_be_logged_out()
		self.browser.refresh()
		self.wait_to_be_logged_out()



	# using selenuim WebDriverWait for 'explicit wait'
	def wait_for_element_with_id(self, element_id):
		WebDriverWait(self.browser, timeout=30).until(
				lambda b: b.find_element_by_id(element_id),
				'Could not find element with if {}. Page text was was {}'.format(
					element_id, self.browser.find_element_by_tag_name('body').text
				)
		)

	# helper
	def switch_to_new_window(self, text_in_title):
		retries = 60
		while retries > 0:
			for handle in self.browser.window_handles:
				self.browser.switch_to_window(handle)
				if text_in_title in self.browser.title:
					return
			retries -= 1
			time.sleep(0.5)
		self.fail('Could not find window')

	def wait_to_be_logged_in(self):
		self.wait_for_element_with_id('id_logout')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn('edith@mockmyid.com', navbar.text)
	
	def wait_to_be_logged_out(self):
		self.wait_for_element_with_id('id_login')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertNotIn('edith@mockmyid.com', navbar.text)
			


