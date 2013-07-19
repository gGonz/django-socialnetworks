from socialnetworks.base.backends import BaseSocialBackend
from socialnetworks.twitter.models import TwitterOAuthProfile


class TwitterBackend(BaseSocialBackend):
    model = TwitterOAuthProfile
