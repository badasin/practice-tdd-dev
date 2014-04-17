import requests
import sys
from accounts.models import ListUser

class PersonaAuthenticationBackend(object):

	def authenticate(self, assertion):
		# send the assertion to Mozilla's verifier service
		data = {'assertion': assertion, 'audience': 'localhost'}
		print('Sending to mozilla', data, file=sys.stderror)
		resp = requests.post('https://verifier.login.persona.org/verify',
				data=data)
		print('Got', resp.content, file=sys.stderror)

		if resp.ok:
			verification_data = resp.json()

			if verification_data['status'] == 'okay':
				email = verification_data['email']
				try:
					return self.get_user(email)
				except ListUser.DoesNotExist:
					return ListUser.objects.create(email=email)
	
	def get_user(self, email):
		return ListUser.objects.get(email=email)
