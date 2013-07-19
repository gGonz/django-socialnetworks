from socialnetworks.base.backends import BaseSocialBackend
from socialnetworks.facebook.models import FacebookOAuthProfile


class FacebookBackend(BaseSocialBackend):
    model = FacebookOAuthProfile
