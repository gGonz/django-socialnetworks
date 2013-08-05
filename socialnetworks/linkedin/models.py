from django.utils.translation import ugettext_lazy as _

from socialnetworks.base.models import BaseOAuth2Profile


class LinkedInOAuthProfile(BaseOAuth2Profile):
    class Meta:
        verbose_name = _('LinkedIn profile')
        verbose_name_plural = _('LinkedIn profiles')
