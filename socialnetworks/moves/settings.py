from django.core.exceptions import ImproperlyConfigured

from ..core.settings import CONFIGURATION, COOKIE_MAX_AGE


# Tries to get the Moves app configuration, if the configuration is not
# provided or is incorrect raises an ImproperlyConfigured exception.
MOVES_APP = CONFIGURATION.get('MOVES_APP', None)

if not MOVES_APP:
    raise ImproperlyConfigured(
        'You have socialnetworks.moves in your ISTALLED_APPS, but you do '
        'not specify any "MOVES_APP" settings inside '
        'SOCIALNETWORK_CONFIGURATION.'
    )

else:
    APP_ID = MOVES_APP.get('APP_ID', None)
    APP_SECRET = MOVES_APP.get('APP_SECRET', None)
    SCOPE = ','.join(MOVES_APP.get('SCOPE', ['activity']))
    SESSION_KEY = MOVES_APP.get('SESSION_KEY', 'dsnmv')
    SESSION_FIELDS = ','.join(MOVES_APP.get('SESSION_FIELDS', []))
    SETUP_URL_NAME = MOVES_APP.get('SETUP_URL_NAME', None)

    if not APP_ID:
        raise ImproperlyConfigured(
            'A proper "APP_ID" must be specified in order to use '
            'socialnetworks.moves module.'
        )

    if not APP_SECRET:
        raise ImproperlyConfigured(
            'A proper "APP_SECRET" must be specified in order to use '
            'socialnetworks.moves module.'
        )
