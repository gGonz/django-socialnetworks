# -*- coding: utf-8 -*-
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from .clients import TwitterClient


def _add_error_message(client, request):
    """
    Adds an error message to the given request, telling that tha user's OAuth
    access token is invalid.
    """
    messages.add_message(request, messages.WARNING, _(
        'Your access token for {service} is invalid. Please connect your '
        'account with your profile again.'
    ).format(service=client.service_name))


def _get_profile_data(client, request):
    """
    Tries to retrieve the Twitter profile data of the given request user or
    returns the error returned by the service.
    """
    response = client.get('account/verify_credentials.json', raw=True)

    if response.status_code != 200:
        _add_error_message(client, request)
        return {'error': response.text}

    return response.json()


def retrieve_twitter_profile(request):
    """
    Returns the current user's Twitter profile data from cache if exists,
    otherwise tries to fetch the data from the service and store it in cache.

    If the user has not Twitter profile returns None.
    """
    if hasattr(request.user, 'twitteroauthprofile'):
        client = TwitterClient(request.user.twitteroauthprofile)
        token_is_valid, data = client.debug_access_token()

        if token_is_valid:
            data = _get_profile_data(client, request)

        else:
            _add_error_message(client, request)

        return data
