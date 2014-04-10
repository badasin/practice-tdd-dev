
from selenium import webdriver
import unittest
## addition
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3) # it won't work on every case
	
	def tearDown(self):
		self.browser.quit()
	
	# helper method
	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows] )

	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get('http://localhost:8000')
		self.assertIn('To-Do', self.browser.title)
		
		# header assertion
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'),
				'Enter a to-do item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER) # import Keys
		self.check_for_row_in_list_table('1: Buy peacock feathers')

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make fly')
		inputbox.send_keys(Keys.ENTER)
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make fly') 
		
		#as a reminder to finish the test
		self.fail('Finish the test!')

if __name__ == '__main__':
	unittest.main(warnings='ignore')

### simple assertion
'''
browser = webdriver.Firefox()
browser.get('http://localhost:8000')

# just simple assertion: assert 'Django' in browser.title
assert 'To-Do' in browser.title

browser.quit()
'''
