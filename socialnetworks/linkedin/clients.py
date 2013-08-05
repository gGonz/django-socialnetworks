from socialnetworks.base.clients import OAuth2Client
from socialnetworks.linkedin import settings
from socialnetworks.linkedin.models import LinkedInOAuthProfile


class LinkedInClient(OAuth2Client):
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

    def get_auth_params(self, token=None):
        # Pass the access token as a parameter for the LinkedIn OAuth2
        # service and tell to return the response in json format.
        if self.profile and not token:
            token = self.profile.oauth_access_token

        return {'format': 'json', 'oauth2_access_token': token}

    def get(self, api_endpoint, params={}, token=None):
        params.update(self.get_auth_params(token))
        url = self.service_api_url + api_endpoint

        return self.__request_get__(url, params=params).json()

    def post(self, api_endpoint, data=None, params={}, token=None):
        params.update(self.get_auth_params(token))
        url = self.service_api_url + api_endpoint

        return self.__request_post__(url, data=data, params=params).json()

    def debug_access_token(self, token=None):
        if self.profile and not token:
            token = self.profile.oauth_access_token

        r = self.get(self.token_debug_url, token=token)

        return (False if 'errorCode' in r else True, r)
