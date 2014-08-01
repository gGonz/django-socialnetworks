from django.utils.translation import ugettext_lazy as _

from ..core.models import BaseOAuth2Profile


class GitHubOAuthProfile(BaseOAuth2Profile):
    """
    Model to store the GitHub OAuth related data.
    """
    class Meta:
        verbose_name = _('github profile')
        verbose_name_plural = _('github profiles')
