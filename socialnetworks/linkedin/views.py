from .clients import LinkedInClient
from .settings import SETUP_URL_NAME
from ..core import views


class LinkedInDialogRedirect(views.OAuthDialogRedirectView):
    """
    View that handles the redirects for the LinkedIn authorization dialog.
    """
    client_class = LinkedInClient


class LinkedInCallback(views.OAuthCallbackView):
    """
    View that handles the LinkedIn OAuth callback.
    """
    client_class = LinkedInClient


class LinkedInSetup(views.OAuthSetupView):
    """
    View that handles the setup of a retrieved LinkedIn account.
    """
    client_class = LinkedInClient
    setup_url = SETUP_URL_NAME


class LinkedInOAuthDisconnect(views.OAuthDisconnectView):
    """
    View that handles the disconnect of a LinkedIn account.
    """
    client_class = LinkedInClient
