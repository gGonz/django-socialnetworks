from socialnetworks.base.utils import read_social_data
from socialnetworks.facebook.settings import SESSION_KEY


def read_facebook_data(request):
    """
    Returns the current user's Facebook data if it was previously fetched
    and stored in the user's session or cookies, otherwise returns None.

    """
    return read_social_data(request, SESSION_KEY)