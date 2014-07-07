from . import settings
from ..base.clients import OAuth2Client
from .models import PayPalOAuthProfile


class PayPalClient(OAuth2Client):
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

    def debug_access_token(self, token=None):
        """
        Check if the given token is valid and can retrieve user info from
        the api.

        """
        if self.profile and not token:
            token = self.profile.oauth_access_token

        r = self.get(self.token_debug_url, auth_params={'access_token': token})

        return ('user_id' in r, r)
