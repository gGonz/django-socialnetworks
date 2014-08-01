from django.core.exceptions import ImproperlyConfigured

from ..core.settings import CONFIGURATION, COOKIE_MAX_AGE


# Tries to get the Twitter configuration, if the configuration is not
# provided or is incorrect raises an ImproperlyConfigured exception.
TWITTER = CONFIGURATION.get('TWITTER', None)

if not TWITTER:
    raise ImproperlyConfigured(
        'You have socialnetworks.facebook in your ISTALLED_APPS, but you do '
        'not specify any "TWITTER" settings inside '
        'SOCIALNETWORK_CONFIGURATION.'
    )

else:
    APP_ID = TWITTER.get('APP_ID', None)
    APP_SECRET = TWITTER.get('APP_SECRET', None)
    SESSION_KEY = TWITTER.get('SESSION_KEY', 'dsntw')
    SESSION_FIELDS = TWITTER.get('SESSION_FIELDS', ['screen_name', 'name'])
    SETUP_URL_NAME = TWITTER.get('SETUP_URL_NAME', None)

    if not APP_ID:
        raise ImproperlyConfigured(
            'A proper "APP_ID" must be specified in order to use '
            'socialnetworks.facebook module.'
        )

    if not APP_SECRET:
        raise ImproperlyConfigured(
            'A proper "APP_SECRET" must be specified in order to use '
            'socialnetworks.facebook module.'
        )
