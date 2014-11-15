import uuid

from . import settings
from .models import GitHubOAuthProfile
from ..core.clients import OAuth2Client


class GitHubClient(OAuth2Client):
    """
    Client to connect to the GitHub REST API.
    """
    # Configuration
    service_name = 'GitHub'
    app_key = settings.APP_ID
    app_secret = settings.APP_SECRET
    app_access_token = settings.APP_ACCESS_TOKEN
    scope = settings.SCOPE
    model = GitHubOAuthProfile

    uid_label = 'id'
    expiration_label = 'expires'

    authorization_url = 'https://github.com/login/oauth/authorize'
    access_token_url = 'https://github.com/login/oauth/access_token'
    token_debug_url = 'user'
    service_api_url = 'https://api.github.com/'
    session_key = 'socialnetworks:github'

    def compose_authorization_url(self, callback_url):
        """
        Return the url to request user authorization at GitHub.
        """
        params = {
            'client_id': self.app_key,
            'redirect_uri': callback_url,
            'scope': self.scope,
            'state': uuid.uuid4()
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

        r = self.get(self.token_debug_url, auth_params={'access_token': token})

        return (False if 'message' in r else True, r)

    def retrieve_user_data(self):
        """
        Return the available data of the user from GitHub.
        """
        r = self.get('user')

        # Parses the "name" of GitHub, simply splits the name by white
        # spaces, the first name is the first element of the resulting list,
        # the last name are the remaining elements joined again by white
        # spaces. If there are not white spaces in the name, then the first
        # name is the name returned by GitHub and the last name is
        # left blak.
        name = r['name']
        first_name = name.split(' ')[0] if ' ' in name else name
        last_name = ' '.join(name.split(' ')[1:]) if ' ' in name else None

        return {
            'username': r['login'],
            'first_name': first_name,
            'last_name': last_name,
            'email': r['email']
        }
