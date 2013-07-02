from socialnetwork.base.backends import BaseSocialBackend
from socialnetwork.twitter.models import TwitterOAuthProfile


class TwitterBackend(BaseSocialBackend):
    model = TwitterOAuthProfile
