from socialnetworks.base.backends import BaseSocialBackend
from socialnetworks.linkedin.models import LinkedInOAuthProfile


class LinkedInBackend(BaseSocialBackend):
    model = LinkedInOAuthProfile
