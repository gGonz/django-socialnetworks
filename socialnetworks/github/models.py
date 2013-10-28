from django.utils.translation import ugettext_lazy as _

from socialnetworks.base.models import BaseOAuth2Profile


class GitHubOAuthProfile(BaseOAuth2Profile):
    class Meta:
        verbose_name = _('github profile')
        verbose_name_plural = _('github profiles')
