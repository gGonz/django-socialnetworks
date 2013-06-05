from socialnetwork.base.backends import BaseSocialBackend
from socialnetwork.facebook.models import FacebookProfile


class FacebookBackend(BaseSocialBackend):
    model = FacebookProfile
