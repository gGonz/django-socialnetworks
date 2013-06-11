from socialnetwork.base.backends import BaseSocialBackend
from socialnetwork.facebook.models import FacebookOAuthProfile


class FacebookBackend(BaseSocialBackend):
    model = FacebookOAuthProfile
