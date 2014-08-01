from django.utils.translation import ugettext_lazy as _

from ..core.models import BaseOAuth2Profile


class PayPalOAuthProfile(BaseOAuth2Profile):
    """
    Model to store the PayPal OAuth related data.
    """
    class Meta:
        verbose_name = _('paypal profile')
        verbose_name_plural = _('paypal profiles')
