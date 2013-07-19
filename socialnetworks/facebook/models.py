from django.utils.translation import ugettext_lazy as _

from socialnetworks.base.models import BaseOAuth2Profile


class FacebookOAuthProfile(BaseOAuth2Profile):
    class Meta:
        verbose_name = _('facebook profile')
        verbose_name_plural = _('facebook profiles')
