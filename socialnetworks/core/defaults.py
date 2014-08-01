from django.utils.translation import ugettext_lazy as _


# Default label for the only login buttons
DEFAULT_LOGIN_LABEL = _('Log in with %(service)s')

# Default label for the login/sigin buttons
DEFAULT_SIGNIN_LABEL = _('Sign in with %(service)s')

# Default message to show when the user is not registered using the only login
# button.
DEFAULT_ERROR_MESSAGE = _(
    'There is no account that matches your %(service)s credentials. You need '
    'to register with your %(service)s account before you can log in with '
    'its credentials.'
)
