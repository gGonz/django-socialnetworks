from django.conf import settings


CLIENT_ID = getattr(
    settings, 'SOCIALNETWORK_FACEBOOK_CLIENT_ID', None
)

CLIENT_SECRET = getattr(
    settings, 'SOCIALNETWORK_FACEBOOK_CLIENT_SECRET', None
)

APP_ACCESS_TOKEN = getattr(
    settings, 'SOCIALNETWORK_FACEBOOK_APP_ACCESS_TOKEN', None
)

EMAIL_IS_USERNAME = getattr(
    settings, 'SOCIALNETWORK_FACEBOOK_EMAIL_IS_USERNAME', True
)

SCOPE = getattr(
    settings, 'SOCIALNETWORK_FACEBOOK_SCOPE_PERMISSIONS', ['email']
)
