from django.utils.translation import ugettext_lazy as _

from ..base.models import BaseOAuth2Profile


class PayPalOAuthProfile(BaseOAuth2Profile):
    class Meta:
        verbose_name = _('paypal profile')
        verbose_name_plural = _('paypal profiles')
