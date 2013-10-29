from socialnetworks.base.utils import read_social_data
from socialnetworks.github.settings import SESSION_KEY


def read_github_data(request):
    """
    Returns the current user's GitHub data if it was previously fetched
    and stored in the user's session or cookies, otherwise returns None.

    """
    return read_social_data(request, SESSION_KEY)
