from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseSocialProfile(models.Model):
    """
    Base model that stores the user's social network information.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        blank=True, null=True,
        verbose_name=_('user')
    )
    service_uid = models.CharField(
        max_length=255,
        unique=True,
        blank=True, null=True,
        verbose_name=_('uid')
    )
    oauth_access_token = models.CharField(
        blank=True, null=True,
        max_length=255,
        verbose_name=_('OAuth access token')
    )

    created_date = models.DateTimeField(
        blank=True, null=True,
        auto_now=False, auto_now_add=True,
        verbose_name=_('created date')
    )
    last_modified = models.DateTimeField(
        null=True, blank=True,
        auto_now_add=True, auto_now=True,
        verbose_name=_('last modified')
    )

    class Meta:
        abstract = True


class BaseOAuth1Profile(BaseSocialProfile):
    """
    Base Model that stores OAuth 1.0 flow information.
    """
    oauth_access_token_secret = models.CharField(
        blank=True, null=True,
        max_length=255,
        verbose_name=_('OAuth access token secret')
    )
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

    class Meta:
        abstract = True


class BaseOAuth2Profile(BaseSocialProfile):
    """
    Base Model that stores OAuth 2.0 flow information.
    """
    oauth_access_token_expires_at = models.DateTimeField(
        blank=True, null=True,
        verbose_name=_('OAuth access token expires at')
    )
    oauth_refresh_token = models.CharField(
        blank=True, null=True,
        max_length=255,
        verbose_name=_('OAuth refresh token')
    )

    class Meta:
        abstract = True
