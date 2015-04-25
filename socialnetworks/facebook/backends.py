# -*- coding: utf-8 -*-
from .models import FacebookOAuthProfile
from ..core.backends import BaseSocialBackend


class FacebookBackend(BaseSocialBackend):
    """
    Backend to handle login with Facebook.
    """
    model = FacebookOAuthProfile
