from .clients import MovesAppClient
from .settings import SETUP_URL_NAME
from ..core import views


class MovesAppDialogRedirect(views.OAuthDialogRedirectView):
    """
    View that handles the redirects for the Moves app authorization dialog.
    """
    client_class = MovesAppClient


class MovesAppCallback(views.OAuthCallbackView):
    """
    View that handles the Moves app OAuth callback.
    """
    client_class = MovesAppClient


class MovesAppSetup(views.OAuthSetupView):
    """
    View that handles the setup of a retrieved Moves app account.
    """
    client_class = MovesAppClient
    setup_url = SETUP_URL_NAME


class MovesAppOAuthDisconnect(views.OAuthDisconnectView):
    """
    View that handles the disconnect of a Moves app account.
    """
    client_class = MovesAppClient
