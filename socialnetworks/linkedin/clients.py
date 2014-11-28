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

    def get_auth_params(self, token=None):
        """
        Compose the authentication params to connect to the LinkedIn API.
        """
        # Pass the access token as a parameter for the LinkedIn OAuth2
        # service and tell to return the response in json format.
        if token is None:
            token = self._oauth_data.get('access_token', None)

        return {'format': 'json', 'oauth2_access_token': token}

    def get(self, api_endpoint, params={}, token=None):
        """
        Method to perform GET requests to the LinkedIn API.
        """
        params.update(self.get_auth_params(token))
        url = self.service_api_url + api_endpoint

        return self._get(url, params=params).json()

    def post(self, api_endpoint, data=None, params={}, token=None):
        """
        Method to perform POST requests to the LinkedIn API.
        """
        params.update(self.get_auth_params(token))
        url = self.service_api_url + api_endpoint

        return self._post(url, data=data, params=params).json()

    def debug_access_token(self, token=None):
        """
        Check if the given access token is yet valid.

        Return a tuple of two objects where the first element is a boolean
        that tells whether the token is valid or not and the second element is
        the data resulting of the token validation.
        """
        if token is None:
            token = self._oauth_data['access_token']

        r = self.get(self.token_debug_url, token=token)

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
