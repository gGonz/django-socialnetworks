from django.utils.translation import ugettext_lazy as _

from ..core.models import BaseOAuth2Profile


class LinkedInOAuthProfile(BaseOAuth2Profile):
    """
    Model to store the LinkedIn OAuth related data.
    """
    class Meta:
        verbose_name = _('LinkedIn profile')
        verbose_name_plural = _('LinkedIn profiles')
