from . import settings
from .models import FacebookOAuthProfile
from ..core.clients import OAuth2Client


class FacebookClient(OAuth2Client):
    """
    Client to connect to the Facebook graph API.
    """
    service_name = 'Facebook'
    app_key = settings.APP_ID
    app_secret = settings.APP_SECRET
    app_access_token = settings.APP_ACCESS_TOKEN
    scope = settings.SCOPE
    model = FacebookOAuthProfile

    expiration_label = 'expires'
    authorization_url = 'https://www.facebook.com/v2.2/dialog/oauth'
    access_token_url = 'https://graph.facebook.com/v2.2/oauth/access_token'
    token_debug_url = 'https://graph.facebook.com/v2.2/debug_token'
    service_api_url = 'https://graph.facebook.com/v2.2/'
    session_key = 'socialnetworks:facebook'

    def compose_authorization_url(self, callback_url):
        """
        Return the url to request user authorization at Facebook.
        """
        params = {
            'client_id': self.app_key,
            'redirect_uri': callback_url,
            'scope': self.scope,
        }

        return self.encode_url(self.authorization_url, params)

    def get_app_access_token(self):
        """
        Returns the app access token if it is defined in settings,
        otherwise fetches the token from Facebook.
        """
        if self.app_access_token:
            return self.app_access_token

        else:
            params = {
                'client_id': self.app_key,
                'client_secret': self.app_secret,
                'grant_type': 'client_credentials'
            }

            r = self._get(self.access_token_url, params=params)

            return self.parse_response(r.content)['access_token']

    def debug_access_token(self, token=None):
        """
        Check if the given access token is yet valid.

        Return a tuple of two objects where the first element is a boolean
        that tells whether the token is valid or not and the second element is
        the data resulting of the token validation.
        """
        if token is None:
            token = self._oauth_data['access_token']

        params = {
            'input_token': token,
            'access_token': self.get_app_access_token()
        }

        r = self._get(self.token_debug_url, params=params)
        data = r.json()

        return (data['data']['is_valid'], data['data'])

    def retrieve_user_data(self):
        """
        Return the available data of the user from Facebook.
        """
        # Defines the fields to retrieve.
        fields = ','.join(['first_name', 'last_name', 'email'])

        return self.get('me', params={'fields': fields})
