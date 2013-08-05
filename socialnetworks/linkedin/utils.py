from socialnetworks.base.utils import read_social_data
from socialnetworks.linkedin.settings import SESSION_KEY


def read_linkedin_data(request):
    """
    Returns the current user's LinkedIn data if it was previously fetched
    and stored in the user's session or cookies, otherwise returns None.

    """
    return read_social_data(request, SESSION_KEY)
