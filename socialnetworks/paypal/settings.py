from django.core.exceptions import ImproperlyConfigured

from ..core.settings import CONFIGURATION, COOKIE_MAX_AGE


# Tries to get the PayPal configuration, if the configuration is not
# provided or is incorrect raises an ImproperlyConfigured exception.
PAYPAL = CONFIGURATION.get('PAYPAL', None)

if not PAYPAL:
    raise ImproperlyConfigured(
        'You have socialnetworks.paypal in your ISTALLED_APPS, but you do '
        'not specify any "PAYPAL" settings inside '
        'SOCIALNETWORKS_CONFIGURATION.'
    )

else:
    APP_ID = PAYPAL.get('APP_ID', None)
    APP_SECRET = PAYPAL.get('APP_SECRET', None)
    APP_ACCESS_TOKEN = PAYPAL.get('APP_ACCESS_TOKEN', None)
    SCOPE = ' '.join(PAYPAL.get('SCOPE', ['openid', 'email']))
    SESSION_KEY = PAYPAL.get('SESSION_KEY', 'dsnpp')
    SESSION_FIELDS = ','.join(PAYPAL.get('SESSION_FIELDS', []))
    IS_LIVE = PAYPAL.get('IS_LIVE', False)
    SETUP_URL_NAME = PAYPAL.get('SETUP_URL_NAME', None)

    if not APP_ID:
        raise ImproperlyConfigured(
            'A proper "APP_ID" must be specified in order to use '
            'socialnetworks.paypal module.'
        )

    if not APP_SECRET:
        raise ImproperlyConfigured(
            'A proper "APP_SECRET" must be specified in order to use '
            'socialnetworks.paypal module.'
        )
