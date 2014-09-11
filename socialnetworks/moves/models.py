from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..core.models import BaseOAuth2Profile


class MovesAppOAuthProfile(BaseOAuth2Profile):
    """
    Model to store the Moves app OAuth related data.
    """
    class Meta:
        verbose_name = _('moves app profile')
        verbose_name_plural = _('moves app profiles')
