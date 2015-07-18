import uuid

from . import settings
from .models import LinkedInOAuthProfile
from ..core.clients import OAuth2Client


class LinkedInClient(OAuth2Client):
    """
    Client to connect to the LinkedIn REST API.
    """
    # Configuration
    service_name = 'LinkedIn'
    app_key = settings.APP_ID
    app_secret = settings.APP_SECRET
    model = LinkedInOAuthProfile

    uid_label = 'id'
    expiration_label = 'expires_in'

    service_api_url = 'https://api.linkedin.com/v1/'
    authorization_url = 'https://www.linkedin.com/uas/oauth2/authorization'
    access_token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'
    token_debug_url = 'people/~:(id)'
    session_key = 'socialnetworks:linkedin'

    def compose_authorization_url(self, callback_url):
        """
        Return the url to request user authorization at LinkedIn.
        """
        params = {
            'client_id': self.app_key,
            'redirect_uri': callback_url,
            'response_type': 'code',
            'scope': self.scope,
            'state': uuid.uuid4(),
        }

        return self.encode_url(self.authorization_url, params)

    def get(self, endpoint, params={}, headers={}, auth=None, raw=False):
        """
        Method to perform GET requests to the LinkedIn API.
        """
        params.update(format='json')
        return super(LinkedInClient, self).get(
            endpoint, params=params, headers=headers, auth=auth, raw=raw)

    def post(self, endpoint, data=None, params={}, headers={},
             auth=None, raw=False):
        """
        Method to perform POST requests to the LinkedIn API.
        """
        params.update(format='json')
        return super(LinkedInClient, self).post(
            endpoint,
            data=data,
            params=params,
            headers=headers,
            auth=auth,
            raw=raw
        )

    def debug_access_token(self, token=None):
        """
        Check if the given access token is yet valid.

        Return a tuple of two objects where the first element is a boolean
        that tells whether the token is valid or not and the second element is
        the data resulting of the token validation.
        """
        if token is None:
            token = self._oauth_data['access_token']

        auth = self.compose_auth({'access_token': token})
        r = self.get(self.token_debug_url, auth=auth)

        return (False if 'errorCode' in r else True, r)

    def retrieve_user_data(self):
        """
        Return the available data of the user from LinkedIn.
        """
        # Defines the fields to retrieve.
        fields = ','.join(['firstName', 'lastName', 'email-address'])

        # Fetches the user's data from the API.
        r = self.get('people/~:(%s)' % fields)

        return {
            'first_name': r['firstName'],
            'last_name': r['lastName'],
            'email': r['emailAddress'],
        }
