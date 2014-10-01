import pytz

from datetime import datetime
from random import randint

from django.contrib.auth import get_user_model
from django.core import signing

from unidecode import unidecode

from .settings import COOKIE_MAX_AGE


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


def compose_username(data):
    """
    Returns a suggested username for a new user.

    If username is passed as a key in the given data dictionary it will be
    used as a base for the suggestion, otherwise the base will be generated by
    the concatenation of the fist and last name of the given data.
    Then the base will be unidecoded and space cleaned and then it will be
    concatenated with a random number between 1 and 9999.
    """
    UserModel = get_user_model()

    if 'username' in data and data['username']:
        raw_name = data['username']

    else:
        raw_name = data['first_name'] + data['last_name']

    unidecoded_name = unidecode(raw_name.replace(' ', ''))
    randomize = lambda n: '%s%d' % (n, randint(1, 9999))
    valid = False

    while not valid:
        username = randomize(unidecoded_name)

        if not UserModel.objects.filter(username__iexact=username):
            valid = True

    return username


def to_timestamp(date_time):
    """
    Transform a Python datetime object to a UNIX UTC timestamp.
    """
    utc_dt = date_time.replace(tzinfo=pytz.UTC)
    delta = utc_dt - datetime(1970, 1, 1, tzinfo=pytz.UTC)

    return delta.total_seconds()


def from_timestamp(timestamp):
    """
    Transform a UNIX UTC timestamp to a Python datetime object.
    """
    return datetime.fromtimestamp(timestamp, tz=pytz.UTC)
