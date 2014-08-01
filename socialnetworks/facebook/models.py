from django.utils.translation import ugettext_lazy as _

from ..core.models import BaseOAuth2Profile


class FacebookOAuthProfile(BaseOAuth2Profile):
    """
    Model to store the Facebook OAuth related data.
    """
    class Meta:
        verbose_name = _('facebook profile')
        verbose_name_plural = _('facebook profiles')
