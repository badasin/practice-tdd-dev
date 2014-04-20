from mock import patch
from django.test import TestCase
from django.conf import settings
from accounts.authentication import (
		PERSONA_VERIFY_URL, PersonaAuthenticationBackend
)
from django.contrib.auth import get_user_model

User = get_user_model()


class GetUserTest(TestCase):

	@patch('accounts.authentication.User.objects.get')
	def test_gets_user_from_ORM_using_email(self, mock_User_get):
		backend = PersonaAuthenticationBackend()
		found_user = backend.get_user('a@b.com')
		self.assertEqual(found_user, mock_User_get.return_value)
		mock_User_get.assert_called_once_with(email='a@b.com')
	
	@patch('accounts.authentication.User.objects.get')
	def test_returns_None_if_user_does_not_exist(self,
			mock_User_get):
		def raise_no_user_error(*_, **__):
			raise User.DoesNotExist()
		mock_User_get.side_effect = raise_no_user_error
		backend = PersonaAuthenticationBackend()
		self.assertIsNone(backend.get_user('a@b.com'))
	



@patch('accounts.authentication.requests.post')
class AuthenticateTest(TestCase):

	def setUp(self):
		self.backend = PersonaAuthenticationBackend()
		#user = User(email='other@user.com')
		#user.name = 'otheruser'
		#user.save()
		#User.objects.create(email='other@user.com')

	def test_sends_assertion_to_Mozilla_with_domain(self, mock_post):
		self.backend.authenticate('an assertion')
		mock_post.assert_called_once_with(
				PERSONA_VERIFY_URL,
				data={'assertion': 'an assertion', 'audience': settings.DOMAIN }
		)
	
	def test_returns_None_if_response_errors(self, mock_post):
		mock_post.return_value.ok = False
		mock_post.return_value.json.return_value = {}
		user = self.backend.authenticate('an assertion')
		self.assertIsNone(user)
	
	def test_returns_None_if_status_not_okay(self, mock_post):
		mock_post.return_value.json.return_value = {'status': 'not okay!'}
		user = self.backend.authenticate('an assertion')
		self.assertIsNone(user)
	
	def test_finds_existing_user_with_email(self, mock_post):
		mock_post.return_value.json.return_value = {
				'status': 'okay', 'email': 'a@b.com'}
		actual_user = User.objects.create(email='a@b.com')
		found_user = self.backend.authenticate('an assertion')
		self.assertEqual(found_user, actual_user)

	def test_creates_new_user_if_necessary_for_valid_assertion(
			self, mock_post):
		mock_post.return_value.json.return_value = {
				'status': 'okay', 'email': 'a@b.com'}
		found_user = self.backend.authenticate('an assertion')
		new_user = User.objects.get(email='a@b.com')
		self.assertEqual(found_user, new_user)


