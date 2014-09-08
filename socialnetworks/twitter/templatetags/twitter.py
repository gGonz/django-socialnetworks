import requests

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from ...core.defaults import (
    DEFAULT_ERROR_MESSAGE, DEFAULT_LOGIN_LABEL, DEFAULT_SIGNIN_LABEL)


register = template.Library()


@register.simple_tag(takes_context=True)
def twitter_login(context, label=None, css_class=None, icon_class=None,
                  only_login=False, error_message=None, error_class=None):
    """
    Renders a 'Sign in with Twitter' button.

    Parameters:
        - label: text to show as button label.
        - css_class: css class to apply to the button.
        - icon_class: css class to apply to the empty <i> tag placed inside
            (left) of the button, useful if used with css icons like
            "Font Awesome" or "Glyphicons".
        - only_login: if True the button will only try to log the user in
            without registering it, if an user that matches the Twitter
            credentials is not found then the user will be redirected to the
            page where the button was originally displayed and an a error
            message will be shown.
        - error_message: text to show as login error, if applicable.
        - error_class: css class to render the error message, if applicable.
    """
    replacements = {
        'service': 'Twitter'
    }

    context['action'] = reverse('socialnetworks:twitter:login')
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
        'twitter/login_button.html', context)


@register.simple_tag(takes_context=True)
def twitter_share(context, label=None, css_class=None, icon_class=None,
                  **kwargs):
    """
    Renders a 'Tweet' button to share content on Twitter.

    Parameters:
        - label: the text to show as button label.
        - css_class: the class to apply to the button

    Keyword arguments:
        - hashtags: Comma separated hashtags appended to tweet text.
        - related: Related accounts.
        - text: Default Tweet text.
        - url: URL of the page to share.
        - via: Screen name of the user to attribute the Tweet to.

    Please visit https://dev.twitter.com/docs/tweet-button for a detailed
    reference of the arguments supported by Twitter.
    """
    # Base javascript for the button.
    base_script = (
        "javascript:(function(){window.twttr=window.twttr||{};var D=550,"
        "A=450,C=screen.height,B=screen.width,H=Math.round((B/2)-(D/2)),"
        "G=0,F=document,E;if(C>A){G=Math.round((C/2)-(A/2))}"
        "window.twttr.shareWin=window.open('%(__URL__)s','','left='+H+',"
        "top='+G+',width='+D+',height='+A+',personalbar=0,toolbar=0,"
        "scrollbars=1,resizable=1');E=F.createElement('script');"
        "E.src=('https:'==document.location.protocol?'https://':'http://')+"
        "'platform.twitter.com/widgets.js';"
        "F.getElementsByTagName('head')[0].appendChild(E)}());"
    )

    # Preparing the url with the encoded parameters.
    r = requests.Request(
        url='https://twitter.com/share', params=kwargs).prepare()

    context['label'] = label or _('Tweet')
    context['css_class'] = css_class
    context['icon_class'] = icon_class
    context['script'] = base_script % {'__URL__': r.url}

    return template.loader.render_to_string(
        'twitter/share_button.html', context)
