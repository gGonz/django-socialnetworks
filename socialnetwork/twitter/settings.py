from django.core.exceptions import ImproperlyConfigured

from socialnetwork.base.settings import CONFIGURATION


# Tries to get the Twitter configuration, if the configuration is not
# provided or is incorrect raises an ImproperlyConfigured exception.
TWITTER = CONFIGURATION.get('TWITTER', None)

if not TWITTER:
    raise ImproperlyConfigured('You have socialnetwork.facebook in your '
        'ISTALLED_APPS, but you do not specify any "TWITTER" settings '
        'inside SOCIALNETWORK_CONFIGURATION.')

else:
    APP_ID = TWITTER.get('APP_ID', None)
    APP_SECRET = TWITTER.get('APP_SECRET', None)

    if not APP_ID:
        raise ImproperlyConfigured('A proper "APP_ID" must be specified '
            'in order to use socialnetwork.facebook module.')

    if not APP_SECRET:
        raise ImproperlyConfigured('A proper "APP_SECRET" must be specified '
            'in order to use socialnetwork.facebook module.')
