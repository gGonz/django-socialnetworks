from .clients import FacebookClient
from .settings import SETUP_URL_NAME
from ..core import views


class FacebookDialogRedirect(views.OAuthDialogRedirectView):
    """
    View that handles the redirects for the Facebook authorization dialog.
    """
    client_class = FacebookClient


class FacebookCallback(views.OAuthCallbackView):
    """
    View that handles the Facebook OAuth callback.
    """
    client_class = FacebookClient


class FacebookSetup(views.OAuthSetupView):
    """
    View that handles the setup of a retrieved Facebook account.
    """
    client_class = FacebookClient
    setup_url = SETUP_URL_NAME


class FacebookOAuthDisconnect(views.OAuthDisconnectView):
    """
    View that handles the disconnect of a Facebook account.
    """
    client_class = FacebookClient
