from datetime import timedelta

from django.utils.timezone import now

from . import settings
from .models import MovesAppOAuthProfile
from ..core.clients import OAuth2Client


class MovesAppClient(OAuth2Client):
    """
    Client to connect to the Moves app API.
    """
    service_name = 'Moves app'
    app_key = settings.APP_ID
    app_secret = settings.APP_SECRET
    scope = settings.SCOPE
    model = MovesAppOAuthProfile

    expiration_label = 'expires_in'
    authorization_url = 'https://api.moves-app.com/oauth/v1/authorize'
    access_token_url = 'https://api.moves-app.com/oauth/v1/access_token'
    token_debug_url = 'https://api.moves-app.com/oauth/v1/tokeninfo'
    refresh_token_url = 'https://api.moves-app.com/oauth/v1/access_token'
    service_api_url = 'https://api.moves-app.com/api/1.1/'
    session_key = 'socialnetworks:moves-app'

    def compose_authorization_url(self, callback_url):
        """
        Return the url to request user authorization at Moves app.
        """
        params = {
            'response_type': 'code',
            'client_id': self.app_key,
            'redirect_uri': callback_url,
            'scope': self.scope,
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

        params = {'access_token': token}

        response = self._get(self.token_debug_url, params=params)

        return (response.status_code == 200, response.json())

    def refresh_access_token(self, update=True):
        """
        Perform a request to the Moves app API to refresh the access token for
        the given profile.

        Return a tuple of two objects where the first element is a boolean
        telling whether the refresh request was successfull and the secons
        element is the data returned by the Moves app API.

        To call this method, client instances must be initialized with a
        proper ```MovesAppOAuthProfile``` instance.

        Pass update=True to force the profile instance to be updated with the
        retrieved data.
        """
        assert isinstance(self._profile, self.model)

        params = {
            'grant_type': 'refresh_token',
            'refresh_token': self._profile.oauth_refresh_token,
            'client_id': self.app_key,
            'client_secret': self.app_secret
        }

        response = self._post(self.refresh_token_url, params=params)
        response_data = response.json()

        if update and response.status_code == 200:
            self._profile.oauth_access_token = response_data.get(
                self.access_token_label)

            self._profile.oauth_refresh_token = response_data.get(
                self.refresh_token_label)

            self._profile.oauth_token_expires_at = now() + timedelta(
                seconds=int(response_data.get(self.expiration_label)))

            self._profile.save()

        return (response.status_code == 200, response.json())
