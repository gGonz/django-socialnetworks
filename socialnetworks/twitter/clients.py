from . import settings
from .models import TwitterOAuthProfile
from ..core.clients import OAuth1Client


class TwitterClient(OAuth1Client):
    """
    Client to connect to the Twitter REST API.
    """
    # Configuration
    service_name = 'Twitter'
    app_key = settings.APP_ID
    app_secret = settings.APP_SECRET
    model = TwitterOAuthProfile

    service_api_url = 'https://api.twitter.com/1.1/'
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    authorization_url = 'https://api.twitter.com/oauth/authorize'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    token_debug_url = 'account/verify_credentials.json'
    session_key = 'socialnetworks:twitter'

    def compose_authorization_url(self, token):
        """
        Return the url to request user authorization at Twitter.
        """
        params = {'oauth_token': token}

        return self.encode_url(self.authorization_url, params)

    def debug_access_token(self):
        """
        Check if the given access token is yet valid.

        Return a tuple of two objects where the first element is a boolean
        that tells whether the token is valid or not and the second element is
        the data resulting of the token validation.
        """
        r = self.get(self.token_debug_url)

        if 'errors' in r:
            return (False, r)

        else:
            return (True, r)

    def retrieve_user_data(self):
        """
        Return the available data of the user from Twitter.
        """
        r = self.get(self.token_debug_url)

        # Parses the "name" of Twitter, simply splits the name by white
        # spaces, the first name is the first element of the resulting list,
        # the last name are the remaining elements joined again by white
        # spaces. If there are not white spaces in the name, then the first
        # name is the name returned by Twitter and the last name is
        # left blak.
        name = r['name']
        first_name = name.split(' ')[0] if ' ' in name else name
        last_name = ' '.join(name.split(' ')[1:]) if ' ' in name else None

        return {
            'username': r['screen_name'],
            'first_name': first_name,
            'last_name': last_name,
        }
