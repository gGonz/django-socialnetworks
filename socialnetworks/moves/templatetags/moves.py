from django import template
from django.core.urlresolvers import reverse

from ...core.defaults import (
    DEFAULT_ERROR_MESSAGE, DEFAULT_LOGIN_LABEL, DEFAULT_SIGNIN_LABEL)


register = template.Library()


@register.simple_tag(takes_context=True)
def moves_login(context, label=None, css_class=None, icon_class=None,
                only_login=False, error_message=None, error_class=None):
    """
    Renders a 'Sign in with Moves app' button.

    Parameters:
        - label: text to show as button label.
        - css_class: css class to apply to the button.
        - icon_class: css class to apply to the empty <i> tag placed inside
            (left) of the button, useful if used with css icons like
            "Font Awesome" or "Glyphicons".
        - only_login: if True the button will only try to log the user in
            without registering it, if an user that matches the Moves app
            credentials is not found then the user will be redirected to the
            page where the button was originally displayed and an a error
            message will be shown.
        - error_message: text to show as login error, if applicable.
        - error_class: css class to render the error message, if applicable.
    """
    replacements = {
        'service': 'Moves app'
    }

    context['action'] = reverse('socialnetworks:moves-app:login')
    context['css_class'] = css_class
    context['icon_class'] = icon_class
    context['error_class'] = error_class
    context['only_login'] = only_login

    context['label'] = (
        label or
        (DEFAULT_LOGIN_LABEL if only_login else DEFAULT_SIGNIN_LABEL) %
        replacements
    )
    context['error_message'] = (
        error_message or
        DEFAULT_ERROR_MESSAGE % replacements
    )

    return template.loader.render_to_string(
        'moves/login_button.html', context)
