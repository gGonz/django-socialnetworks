from django.utils.translation import ugettext_lazy as _

from socialnetworks.base.models import BaseOAuth1Profile


class TwitterOAuthProfile(BaseOAuth1Profile):
    class Meta:
        verbose_name = _('twitter profile')
        verbose_name_plural = _('twitter profiles')
