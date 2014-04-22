from .base import FunctionalTest

class MyListTest(FunctionalTest):
	
	def test_logged_in_users_lists_are_saved_as_my_lists(self):
		self.create_pre_authenticated_session('edith@mockmyid.com')

		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys('Reticulate splines\n')
		self.get_item_input_box().send_keys('Immanentize eschaton\n')
		first_list_url = self.browser.current_url

		self.browser.find_element_by_link_text('My lists').click()

		self.browser.find_element_by_link_text('Reticulate splines').click()
		self.assertEqual(self.browser.current_url, first_list_url)

		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys('Click cows\n')
		second_list_url = self.browser.current_url

		self.browser.find_element_by_link_text('My lists').click()
		self.browser.find_element_by_link_text('Click cows').click()
		self.assertEqual(self.browser.current_url, second_list_url)
		
		self.browser.find_element_by_id('id_logout').click()
		self.assertEqual(
				self.browser.find_element_by_link_text('My lists'),
				[]
		)

