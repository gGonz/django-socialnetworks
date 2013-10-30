from django.core.urlresolvers import reverse

from socialnetworks.base.views import (
    OAuthDialogRedirectView, OAuthCallbackView,
    OAuthSetupView, OAuthDisconnectView
)
from socialnetworks.facebook.clients import FacebookClient


class FacebookDialogRedirect(OAuthDialogRedirectView):
    client = FacebookClient()

    def get_callback_url(self):
        return self.client.get_domain() + reverse(
            'socialnetworks:facebook:callback')

    def get_redirect_url(self):
        return self.client.encode_url(self.client.authorization_url, {
            'client_id': self.client.app_key,
            'redirect_uri': self.get_callback_url(),
            'scope': self.client.scope,
        })


class FacebookCallback(OAuthCallbackView):
    client = FacebookClient()

    def get_callback_url(self):
        return self.client.get_domain() + reverse(
            'socialnetworks:facebook:callback')

    def get_redirect_url(self):
        if self.session_get('new_user'):
            return reverse('socialnetworks:facebook:setup')

        else:
            return self.session_pop('next') or '/'


class FacebookSetup(OAuthSetupView):
    client = FacebookClient()

    def get_redirect_url(self):
        return self.session_pop('next') or '/'

    def retrieve_user_data(self):
        # Retrieves the proper profile.
        profile = self.get_profile()

        # Creates a client that can make signed requests.
        fb = FacebookClient(profile)

        # Defines the fields to retrieve.
        fields = ','.join(['first_name', 'last_name', 'email', 'username'])

        # Fetches the user's data from Facebook.
        return fb.get('me', params={'fields': fields})


class FacebookOAuthDisconnect(OAuthDisconnectView):
    client = FacebookClient()
