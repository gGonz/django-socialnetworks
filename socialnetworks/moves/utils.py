from .settings import SESSION_KEY
from ..core.utils import read_social_data


def read_moves_app_data(request):
    """
    Returns the current user's Moves app data if it was previously fetched
    and stored in the user's session or cookies, otherwise returns None.
    """
    return read_social_data(request, SESSION_KEY)
