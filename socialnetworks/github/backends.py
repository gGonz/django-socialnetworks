from .models import GitHubOAuthProfile
from ..core.backends import BaseSocialBackend


class GitHubBackend(BaseSocialBackend):
    """
    Backend to handle login with GitHub.
    """
    model = GitHubOAuthProfile
