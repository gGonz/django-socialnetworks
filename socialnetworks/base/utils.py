from django.core import signing

from socialnetworks.base.settings import COOKIE_MAX_AGE


def read_social_data(request, key):
    """
    Search the current request for user's social information, search first
    in the user's session, if there is no information then search in the
    request's cookies.

    Returns a dictionary of the social information if found, otherwise
    returns None.

    """
    data = request.session.get(key, request.get_signed_cookie(
        key, max_age=COOKIE_MAX_AGE, default=None))

    return signing.loads(data) if data else None
