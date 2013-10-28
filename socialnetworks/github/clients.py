from socialnetworks.base.clients import OAuth2Client
from socialnetworks.github import settings
from socialnetworks.github.models import GitHubOAuthProfile


class GitHubClient(OAuth2Client):
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

    def debug_access_token(self, token=None):
        if self.profile and not token:
            token = self.profile.oauth_access_token

        r = self.get(self.token_debug_url, auth_params={'access_token': token})

        return (False if 'message' in r else True, r)
