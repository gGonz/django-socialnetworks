from uuid import uuid4

from . import settings
from ..core.clients import OAuth2Client
from .models import PayPalOAuthProfile


class PayPalClient(OAuth2Client):
    """
    Client to connect with the PayPal REST API.
    """
    # Configuration
    service_name = 'PayPal'
    app_key = settings.APP_ID
    app_secret = settings.APP_SECRET
    app_access_token = settings.APP_ACCESS_TOKEN
    scope = settings.SCOPE
    model = PayPalOAuthProfile

    expiration_label = 'expires_in'

    is_live = settings.IS_LIVE
    token_debug_url = 'identity/openidconnect/userinfo/?schema=openid'
    session_key = 'socialnetworks:paypal'

    def get_base_api_domain(self):
        """
        Return the base paypal domain depending in the 'IS_LIVE' setting.
        """
        return 'api.paypal.com' if self.is_live else 'api.sandbox.paypal.com'

    @property
    def authorization_url(self):
        """
        Return the proper authorization url depending in the 'IS_LIVE' setting.
        """
        if self.is_live:
            return ('https://www.paypal.com/webapps/auth/protocol/'
                    'openidconnect/v1/authorize')
        else:
            return ('https://www.sandbox.paypal.com/webapps/auth/protocol/'
                    'openidconnect/v1/authorize')

    @property
    def access_token_url(self):
        """
        Return the proper aacces token url depending in the 'IS_LIVE' setting.
        """
        return ('https://%s/v1/identity/openidconnect/tokenservice' %
                self.get_base_api_domain())

    @property
    def service_api_url(self):
        """
        Return the proper api url depending in the 'IS_LIVE' setting.
        """
        return 'https://%s/v1/' % self.get_base_api_domain()

    def compose_authorization_url(self, callback_url):
        """
        Return the url to request user authorization at PayPal.
        """
        params = {
            'client_id': self.app_key,
            'redirect_uri': callback_url,
            'response_type': 'code',
            'scope': self.scope,
            'nonce': uuid4()
        }

        return self.encode_url(self.authorization_url, params)

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

        return ('user_id' in r, r)

    def retrieve_user_data(self):
        """
        Return the available data of the user from PayPal.
        """
        r = self.get(self.token_debug_url)

        return {
            'first_name': r['given_name'],
            'last_name': r['family_name'],
            'email': r['email']
        }
