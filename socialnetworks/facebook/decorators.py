from functools import wraps

from django.core import signing
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .clients import FacebookClient
from .settings import COOKIE_MAX_AGE, SESSION_FIELDS, SESSION_KEY


def fetch_facebook_data(function):
    """
    Decorator that extends a view to allow it to fetch the user's
    data from Facebook.
    """
    @wraps(function)
    def function_wrapper(request, *args, **kwargs):
        # Check if the key for the Facebook session is in the user's session
        # and deletes it if it is present.
        if SESSION_KEY in request.session:
            del request.session[SESSION_KEY]

        # Tries to create a Facebook client for the current user.
        try:
            client = FacebookClient(request.user.facebookoauthprofile)
        except:
            client = None

        # If the client for this user was successfully created and the
        # user's data is not retrieved yet from Facebook: checks the
        # validity of the current access token, if the token is valid
        # retrieves the data from Facebook, if the token is invalid then
        # requests a new token.
        if client and SESSION_KEY not in request.COOKIES:
            if not client.debug_access_token():

                return HttpResponseRedirect(reverse(
                    'socialnetworks:facebook:login'))

            else:
                # Retrieves the data from Facebook.
                data = client.get('me', params={'fields': SESSION_FIELDS})

                # Protects the user potentially sensible data.
                data = signing.dumps(data)

                # Stores the retrieved data temporarily in the user session
                # if required to access it in the view.
                request.session[SESSION_KEY] = data

                # Creates the response object and stores the retrieved data
                # in a signed cookie that its valid only for the seconds
                # specified in settings.
                response = function(request, *args, **kwargs)
                response.set_signed_cookie(
                    SESSION_KEY, value=data,
                    httponly=True, max_age=COOKIE_MAX_AGE
                )

                return response

        # If there is no client for the current user but it has data stored
        # in its session (when a user disconnects its profile), removes
        # the data from its cookies.
        elif not client and SESSION_KEY in request.COOKIES:
            # Stores temporarily a empty data for the session, this way
            # we can check quickly in the view if the user has disconnected
            # its profile.
            request.session[SESSION_KEY] = None

            # Creates the response object and deletes the cookie from it.
            response = function(request, *args, **kwargs)
            response.delete_cookie(SESSION_KEY)

            return response

        return function(request, *args, **kwargs)

    return function_wrapper
