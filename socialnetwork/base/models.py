from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class BaseSocialProfile(models.Model):
    """
    Base model that stores the user's social network information.

    """
    user = models.OneToOneField(
        User,
        blank=True, null=True,
        verbose_name=_('user')
    )
    service_uid = models.CharField(
        max_length=80,
        unique=True,
        blank=True, null=True,
        verbose_name=_('uid')
    )
    last_modified = models.DateTimeField(
        null=True, blank=True,
        auto_now_add=True, auto_now=True,
        verbose_name=_('last modified')
    )

    class Meta:
        abstract = True


class BaseOAuthProfile(BaseSocialProfile):
    """
    Base Model that stores OAuth 1.0 flow information.

    """
    oauth_request_token = models.CharField(
        blank=True, null=True,
        max_length=255,
        verbose_name=_('OAuth request token')
    )
    oauth_request_token_secret = models.CharField(
        blank=True, null=True,
        max_length=255,
        verbose_name=_('OAuth request token secret')
    )
    oauth_access_token = models.CharField(
        blank=True, null=True,
        max_length=255,
        verbose_name=_('OAuth access token')
    )
    oauth_access_token_secret = models.CharField(
        blank=True, null=True,
        max_length=255,
        verbose_name=_('OAuth access token secret')
    )

    class Meta:
        abstract = True


class BaseOAuth2Profile(BaseSocialProfile):
    """
    Base Model that stores OAuth 2.0 flow information.

    """
    oauth_access_token = models.CharField(
        blank=True, null=True,
        max_length=255,
        verbose_name=_('OAuth access token')
    )
    oauth_access_token_expires_at = models.DateTimeField(
        blank=True, null=True,
        verbose_name=_('OAuth access token expires at')
    )

    class Meta:
        abstract = True
