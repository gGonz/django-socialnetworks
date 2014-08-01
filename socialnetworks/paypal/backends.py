from .models import PayPalOAuthProfile
from ..core.backends import BaseSocialBackend


class PayPalBackend(BaseSocialBackend):
    """
    Backend to handle login with PayPal.
    """
    model = PayPalOAuthProfile
