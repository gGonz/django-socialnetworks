import requests

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from socialnetwork.base.clients import BaseOAuth2Client
from socialnetwork.facebook import settings
from socialnetwork.facebook.models import FacebookProfile


class FacebookClient(BaseOAuth2Client):
    service_name = 'Facebook'

    # Facebook configuration loaded from the settings.
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    app_access_token = settings.APP_ACCESS_TOKEN
    scope = ','.join(settings.SCOPE)
    email_is_username = settings.EMAIL_IS_USERNAME

    # Facebook manual configuration.
    login_dialog_endpoint = 'https://www.facebook.com/dialog/oauth?'
    access_token_endpoint = 'https://graph.facebook.com/oauth/access_token?'
    api_entrypoint = 'https://graph.facebook.com/'
    session_key = 'socialnetwork:facebook'
    model = FacebookProfile

    # Facebook callback url.
    def get_callback_url(self):
        return 'http://%(domain)s%(callback)s' % {
            'domain': Site.objects.get_current(),
            'callback': reverse('socialnetwork:facebook:callback')
        }

    # Returns the app access token if it is defined in settings,
    # otherwise fetches the token from Facebook.
    def get_app_access_token(self):
        if self.app_access_token:
            return self.app_access_token

        else:
            response = requests.get(
                'https://graph.facebook.com/oauth/access_token?',
                params={
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'grant_type': 'client_credentials'
                }
            )

            content = self.parse_access_token(response.content)
            return content['access_token']

    # Connects with Facebook to debug the given access token.
    def debug_access_token(self, token):
        response = self.request(
            self.api_entrypoint + 'debug_token?',
            params={'input_token': token},
            signature={'access_token': self.get_app_access_token()}
        )

        if 'data' in response and response['data']['is_valid']:
            return (True, response['data'])
        else:
            return (False, None)


class FacebookGraph(FacebookClient):
    """
    Client to explore the Facebook Graph API.

    This client should not be used directly, it is defined as an attribute
    in the FacebookClient class.

    """
    def __init__(self, profile):
        self.profile = profile

    def debug_access_token(self):
        return super(FacebookGraph, self).debug_access_token(self.profile.oauth_access_token)

    def compose_signature(self):
        """
        Returns the proper signature for the oauth requests.

        """
        return {'access_token': self.profile.oauth_access_token}

    def get(self, endpoint, params={}, headers={}, signature=None):
        """
        GET method to the Facebook Graph API.

        """
        return self.request(
            self.api_entrypoint + endpoint,
            params=params, headers=headers,
            signature=signature or self.compose_signature()
        )
