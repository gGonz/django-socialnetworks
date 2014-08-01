from django.core.exceptions import ImproperlyConfigured

from ..core.settings import CONFIGURATION, COOKIE_MAX_AGE


# Tries to get the GitHub configuration, if the configuration is not
# provided or is incorrect raises an ImproperlyConfigured exception.
GITHUB = CONFIGURATION.get('GITHUB', None)

if not GITHUB:
    raise ImproperlyConfigured(
        'You have socialnetworks.github in your ISTALLED_APPS, but you do '
        'not specify any "GITHUB" settings inside '
        'SOCIALNETWORK_CONFIGURATION.'
    )

else:
    APP_ID = GITHUB.get('APP_ID', None)
    APP_SECRET = GITHUB.get('APP_SECRET', None)
    APP_ACCESS_TOKEN = GITHUB.get('APP_ACCESS_TOKEN', None)
    SCOPE = ','.join(GITHUB.get('SCOPE', ['email']))
    SESSION_KEY = GITHUB.get('SESSION_KEY', 'dsnfb')
    SESSION_FIELDS = ','.join(GITHUB.get('SESSION_FIELDS', []))
    SETUP_URL_NAME = GITHUB.get('SETUP_URL_NAME', None)

    if not APP_ID:
        raise ImproperlyConfigured(
            'A proper "APP_ID" must be specified in order to use '
            'socialnetworks.github module.'
        )

    if not APP_SECRET:
        raise ImproperlyConfigured(
            'A proper "APP_SECRET" must be specified in order to use '
            'socialnetworks.github module.'
        )
