import uuid

from django.core.urlresolvers import reverse

from socialnetworks.base.views import (
    OAuthDialogRedirectView, OAuthCallbackView,
    OAuthSetupView, OAuthDisconnectView
)
from socialnetworks.linkedin.clients import LinkedInClient


class LinkedInDialogRedirect(OAuthDialogRedirectView):
    client = LinkedInClient()

    def get_callback_url(self):
        return self.client.get_domain() + reverse(
            'socialnetworks:linkedin:callback')

    def get_redirect_url(self):
        return self.client.encode_url(self.client.authorization_url, {
            'client_id': self.client.app_key,
            'redirect_uri': self.get_callback_url(),
            'response_type': 'code',
            'scope': self.client.scope,
            'state': uuid.uuid4(),
        })


class LinkedInCallback(OAuthCallbackView):
    client = LinkedInClient()

    def get_callback_url(self):
        return self.client.get_domain() + reverse(
            'socialnetworks:linkedin:callback')

    def get_redirect_url(self):
        if self.session_get('new_user'):
            return reverse('socialnetworks:linkedin:setup')

        else:
            return self.session_pop('next') or '/'


class LinkedInSetup(OAuthSetupView):
    client = LinkedInClient()

    def get_redirect_url(self):
        return self.session_pop('next') or '/'

    def retrieve_user_data(self):
        # Retrieves the proper profile.
        profile = self.get_profile()

        # Creates a client that can make signed requests.
        li = LinkedInClient(profile)

        # Defines the fields to retrieve.
        fields = ','.join(['firstName', 'lastName', 'email-address'])

        # Fetches the user's data from LinkedIn.
        r = li.get('people/~:(%s)' % fields)

        return {
            'first_name': r['firstName'],
            'last_name': r['lastName'],
            'email': r['emailAddress'],
        }


class LinkedInOAuthDisconnect(OAuthDisconnectView):
    client = LinkedInClient()
