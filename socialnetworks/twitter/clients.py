from socialnetworks.base.clients import OAuth1Client
from socialnetworks.twitter import settings
from socialnetworks.twitter.models import TwitterOAuthProfile


class TwitterClient(OAuth1Client):
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

    def debug_access_token(self):
        if self.profile:
            r = self.get(self.token_debug_url)

            if 'errors' in r:
                return (False, r)
            else:
                return (True, r)
