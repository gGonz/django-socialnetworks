from django.utils.translation import ugettext_lazy as _

from ..core.models import BaseOAuth1Profile


class TwitterOAuthProfile(BaseOAuth1Profile):
    """
    Model to store the Twitter OAuth related data.
    """
    class Meta:
        verbose_name = _('twitter profile')
        verbose_name_plural = _('twitter profiles')
