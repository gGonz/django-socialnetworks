# -*- coding: utf-8 -*-
from .models import LinkedInOAuthProfile
from ..core.backends import BaseSocialBackend


class LinkedInBackend(BaseSocialBackend):
    """
    Backend to handle login with LinkedIn.
    """
    model = LinkedInOAuthProfile
