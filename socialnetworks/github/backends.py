from socialnetworks.base.backends import BaseSocialBackend
from socialnetworks.github.models import GitHubOAuthProfile


class GitHubBackend(BaseSocialBackend):
    model = GitHubOAuthProfile
