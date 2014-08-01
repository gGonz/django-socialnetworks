from .clients import GitHubClient
from .settings import SETUP_URL_NAME
from ..core import views


class GitHubDialogRedirect(views.OAuthDialogRedirectView):
    """
    View that handles the redirects for the GitHub authorization dialog.
    """
    client_class = GitHubClient


class GitHubCallback(views.OAuthCallbackView):
    """
    View that handles the GitHub OAuth callback.
    """
    client_class = GitHubClient


class GitHubSetup(views.OAuthSetupView):
    """
    View that handles the setup of a retrieved GitHub account.
    """
    client_class = GitHubClient
    setup_url = SETUP_URL_NAME


class GitHubOAuthDisconnect(views.OAuthDisconnectView):
    """
    View that handles the disconnect of a GitHub account.
    """
    client_class = GitHubClient
