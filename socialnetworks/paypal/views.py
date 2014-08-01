from .clients import PayPalClient
from .settings import SETUP_URL_NAME
from ..core import views


class PayPalDialogRedirect(views.OAuthDialogRedirectView):
    """
    View that handles the redirects for the PayPal authorization dialog.
    """
    client_class = PayPalClient
#    def get_redirect_url(self):
#        return self.client.encode_url(self.client.authorization_url, {
#            'client_id': self.client.app_key,
#            'redirect_uri': self.get_callback_url(),
#            'response_type': 'code',
#            'scope': self.client.scope,
#            'nonce': uuid4()
#        })


class PayPalCallback(views.OAuthCallbackView):
    """
    View that handles the PayPal OAuth callback.
    """
    client_class = PayPalClient
#    def get_redirect_url(self):
#        if self.session_get('new_user'):
#            return reverse('socialnetworks:paypal:setup')
#
#        else:
#            return self.session_pop('next') or '/'


class PayPalSetup(views.OAuthSetupView):
    """
    View that handles the setup of a retrieved PayPal account.
    """
    client_class = PayPalClient
    setup_url = SETUP_URL_NAME
#    def retrieve_user_data(self):
#        # Retrieves the proper profile.
#        profile = self.get_profile()
#
#        # Creates a client that can make signed requests.
#        pp = PayPalClient(profile)
#
#        # Retrieve the user info from the api.
#        data = pp.get(pp.token_debug_url)
#
#        return {
#            'first_name': data['given_name'],
#            'last_name': data['family_name'],
#            'email': data['email']
#        }


class PayPalOAuthDisconnect(views.OAuthDisconnectView):
    """
    View that handles the disconnect of a PayPal account.
    """
    client_class = PayPalClient
