# -*- coding: utf-8 -*-
from .models import TwitterOAuthProfile
from ..core.backends import BaseSocialBackend


class TwitterBackend(BaseSocialBackend):
    """
    Backend to handle login with Twitter.
    """
    model = TwitterOAuthProfile
