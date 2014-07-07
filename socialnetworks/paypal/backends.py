from .models import PayPalOAuthProfile
from ..base.backends import BaseSocialBackend


class PayPalBackend(BaseSocialBackend):
    model = PayPalOAuthProfile
