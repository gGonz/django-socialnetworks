import importlib

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


__all__ = ['EMAIL_IS_USERNAME', 'SETUP_FORM_CLASS', 'SETUP_TEMPLATE']

# Tries to get the module configuration, if the configuration is not
# provided or is incorrect raises an ImproperlyConfigured exception.
if [True for app in settings.INSTALLED_APPS if 'socialnetwork' in app]:
    CONFIGURATION = getattr(settings, 'SOCIALNETWORKS_CONFIGURATION', None)

    if not CONFIGURATION:
        raise ImproperlyConfigured(
            'You have one or more socialnetworks modules in your '
            'INSTALLED_APPS but you do not specify any '
            '"SOCIALNETWORKS_CONFIGURATION" in your settings.'
        )

    else:
        EMAIL_IS_USERNAME = CONFIGURATION.get('EMAIL_IS_USERNAME', True)
        COOKIE_MAX_AGE = CONFIGURATION.get('COOKIE_MAX_AGE', 900)
        SETUP_TEMPLATE = CONFIGURATION.get(
            'SETUP_TEMPLATE',
            'setup_form.html'
        )
        ACTIVATE_ALREADY_REGISTERED_USERS = CONFIGURATION.get(
            'ACTIVATE_ALREADY_REGISTERED_USERS',
            False
        )

        # Imports and defines the setup form class.
        form_class = CONFIGURATION.get(
            'SETUP_FORM_CLASS',
            'socialnetworks.core.forms.SocialUserCreationForm'
        )

        module_ = '.'.join(form_class.split('.')[:-1])
        class_ = form_class.split('.')[-1]
        module = importlib.import_module(module_)

        SETUP_FORM_CLASS = getattr(module, class_)
