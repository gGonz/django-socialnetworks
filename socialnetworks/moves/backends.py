from .models import MovesAppOAuthProfile
from ..core.backends import BaseSocialBackend


class MovesAppBackend(BaseSocialBackend):
    """
    Backend to handle login with Moves app.
    """
    model = MovesAppOAuthProfile
