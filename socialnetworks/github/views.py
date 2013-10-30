import uuid

from django.core.urlresolvers import reverse

from socialnetworks.base.views import (
    OAuthDialogRedirectView, OAuthCallbackView,
    OAuthSetupView, OAuthDisconnectView
)
from socialnetworks.github.clients import GitHubClient


class GitHubDialogRedirect(OAuthDialogRedirectView):
    client = GitHubClient()

    def get_callback_url(self):
        return self.client.get_domain() + reverse(
            'socialnetworks:github:callback')

    def get_redirect_url(self):
        return self.client.encode_url(self.client.authorization_url, {
            'client_id': self.client.app_key,
            'redirect_uri': self.get_callback_url(),
            'scope': self.client.scope,
            'state': uuid.uuid4()
        })


class GitHubCallback(OAuthCallbackView):
    client = GitHubClient()

    def get_callback_url(self):
        return self.client.get_domain() + reverse(
            'socialnetworks:github:callback')

    def get_redirect_url(self):
        if self.session_get('new_user'):
            return reverse('socialnetworks:github:setup')

        else:
            return self.session_pop('next') or '/'


class GitHubSetup(OAuthSetupView):
    client = GitHubClient()

    def get_redirect_url(self):
        return self.session_pop('next') or '/'

    def retrieve_user_data(self):
        # Retrieves the proper profile.
        profile = self.get_profile()

        # Creates a client that can make signed requests.
        gh = GitHubClient(profile)

        # Defines the fields to retrieve.
        #fields = ','.join(['first_name', 'last_name', 'email', 'username'])
        data = gh.get('user')

        # Parses the "name" of GitHub, simply splits the name by white
        # spaces, the first name is the first element of the resulting list,
        # the last name are the remaining elements joined again by white
        # spaces. If there are not white spaces in the name, then the first
        # name is the name returned by GitHub and the last name is
        # left blak.
        name = data['name']
        first_name = name.split(' ')[0] if ' ' in name else name
        last_name = ' '.join(name.split(' ')[1:]) if ' ' in name else None

        return {
            'first_name': first_name,
            'last_name': last_name,
            'email': data['email']
        }


class GitHubOAuthDisconnect(OAuthDisconnectView):
    client = GitHubClient()
