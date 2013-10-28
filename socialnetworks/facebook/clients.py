from socialnetworks.base.clients import OAuth2Client
from socialnetworks.facebook import settings
from socialnetworks.facebook.models import FacebookOAuthProfile


class FacebookClient(OAuth2Client):
    # Configuration
    service_name = 'Facebook'
    app_key = settings.APP_ID
    app_secret = settings.APP_SECRET
    app_access_token = settings.APP_ACCESS_TOKEN
    scope = settings.SCOPE
    model = FacebookOAuthProfile

    expiration_label = 'expires'

    authorization_url = 'https://www.facebook.com/dialog/oauth'
    access_token_url = 'https://graph.facebook.com/oauth/access_token'
    token_debug_url = 'debug_token'
    service_api_url = 'https://graph.facebook.com/'
    session_key = 'socialnetworks:facebook'

    # Returns the app access token if it is defined in settings,
    # otherwise fetches the token from Facebook.
    def get_app_access_token(self):
        if self.app_access_token:
            return self.app_access_token

        else:
            params = {
                'client_id': self.app_key,
                'client_secret': self.app_secret,
                'grant_type': 'client_credentials'
            }
            r = self.__request_get__(self.access_token_url, params=params)

            return self.parse_response(r.content)['access_token']

    def debug_access_token(self, token=None):
        if self.profile and not token:
            token = self.profile.oauth_access_token

        r = self.get(
            self.token_debug_url, params={'input_token': token},
            auth_params={'access_token': self.get_app_access_token()}
        )

        if 'data' in r and r['data']['is_valid']:
            return (True, r['data'])

        else:
            return (False, None)
