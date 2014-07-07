from uuid import uuid4

from django.core.urlresolvers import reverse

from .clients import PayPalClient
from ..base import views


class PayPalDialogRedirect(views.OAuthDialogRedirectView):
    client = PayPalClient()

    def get_callback_url(self):
        return self.request.build_absolute_uri(reverse(
            'socialnetworks:paypal:callback'))

    def get_redirect_url(self):
        return self.client.encode_url(self.client.authorization_url, {
            'client_id': self.client.app_key,
            'redirect_uri': self.get_callback_url(),
            'response_type': 'code',
            'scope': self.client.scope,
            'nonce': uuid4()
        })


class PayPalCallback(views.OAuthCallbackView):
    client = PayPalClient()

    def get_callback_url(self):
        return self.request.build_absolute_uri(reverse(
            'socialnetworks:paypal:callback'))

    def get_redirect_url(self):
        if self.session_get('new_user'):
            return reverse('socialnetworks:paypal:setup')

        else:
            return self.session_pop('next') or '/'


class PayPalSetup(views.OAuthSetupView):
    client = PayPalClient()

    def get_redirect_url(self):
        return self.session_pop('next') or '/'

    def retrieve_user_data(self):
        # Retrieves the proper profile.
        profile = self.get_profile()

        # Creates a client that can make signed requests.
        pp = PayPalClient(profile)

        # Retrieve the user info from the api.
        data = pp.get(pp.token_debug_url)

        return {
            'first_name': data['given_name'],
            'last_name': data['family_name'],
            'email': data['email']
        }


class PayPalOAuthDisconnect(views.OAuthDisconnectView):
    client = PayPalClient()
