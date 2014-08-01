from django.core.exceptions import ImproperlyConfigured

from ..core.settings import CONFIGURATION, COOKIE_MAX_AGE


# Tries to get the LINKEDIN configuration, if the configuration is not
# provided or is incorrect raises an ImproperlyConfigured exception.
LINKEDIN = CONFIGURATION.get('LINKEDIN', None)

if not LINKEDIN:
    raise ImproperlyConfigured(
        'You have socialnetworks.linkedin in your ISTALLED_APPS, but you do '
        'not specify any "LINKEDIN" settings inside '
        'SOCIALNETWORK_CONFIGURATION.'
    )

else:
    APP_ID = LINKEDIN.get('APP_ID', None)
    APP_SECRET = LINKEDIN.get('APP_SECRET', None)
    SESSION_KEY = LINKEDIN.get('SESSION_KEY', 'dsnli')
    SESSION_FIELDS = ','.join(LINKEDIN.get(
        'SESSION_FIELDS', ['firstName', 'lastName']))
    SETUP_URL_NAME = LINKEDIN.get('SETUP_URL_NAME', None)

    if not APP_ID:
        raise ImproperlyConfigured(
            'A proper "APP_ID" must be specified in order to use '
            'socialnetworks.linkedin module.'
        )

    if not APP_SECRET:
        raise ImproperlyConfigured(
            'A proper "APP_SECRET" must be specified in order to use '
            'socialnetworks.linkedin module.'
        )
