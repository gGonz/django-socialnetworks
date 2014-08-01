from .clients import TwitterClient
from .settings import SETUP_URL_NAME
from ..core import views


class TwitterDialogRedirect(views.OAuthDialogRedirectView):
    """
    View that handles the redirects for the Twitter authorization dialog.
    """
    client_class = TwitterClient


class TwitterCallback(views.OAuthCallbackView):
    """
    View that handles the Twitter OAuth callback.
    """
    client_class = TwitterClient
    setup_url = SETUP_URL_NAME


class TwitterSetupView(views.OAuthSetupView):
    """
    View that handles the setup of a retrieved Twitter account.
    """
    client_class = TwitterClient


class TwitterOAuthDisconnect(views.OAuthDisconnectView):
    """
    View that handles the disconnect of a Twitter account.
    """
    client_class = TwitterClient
