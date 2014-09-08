from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from ..settings import APP_ID
from ...core.defaults import (
    DEFAULT_ERROR_MESSAGE, DEFAULT_LOGIN_LABEL, DEFAULT_SIGNIN_LABEL)


register = template.Library()


@register.simple_tag(takes_context=True)
def facebook_login(context, label=None, css_class=None, icon_class=None,
                   only_login=False, error_message=None, error_class=None):
    """
    Renders a 'Sign in with Facebook' button.

    Parameters:
        - label: text to show as button label.
        - css_class: css class to apply to the button.
        - icon_class: css class to apply to the empty <i> tag placed inside
            (left) of the button, useful if used with css icons like
            "Font Awesome" or "Glyphicons".
        - only_login: if True the button will only try to log the user in
            without registering it, if an user that matches the Facebook
            credentials is not found then the user will be redirected to the
            page where the button was originally displayed and an a error
            message will be shown.
        - error_message: text to show as login error, if applicable.
        - error_class: css class to render the error message, if applicable.
    """
    replacements = {
        'service': 'Facebook'
    }

    context['action'] = reverse('socialnetworks:facebook:login')
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
        'facebook/login_button.html', context)


@register.simple_tag(takes_context=True)
def facebook_share(context, label=None, css_class=None, icon_class=None,
                   **kwargs):
    """
    Renders a 'Share' button to share content on Facebook.

    Parameters:
        - label: the text to show as button label.
        - css_class: the class to apply to the button.

    Keyword arguments:
        - actions: A JSON array containing a single object describing
            the action link which will appear next to the "Comment" and "Like"
            link under posts.
        - caption: The caption of the link (appears beneath the link name).
        - description: The description of the link (appears beneath the
            link caption).
        - from: The ID or username of the person posting the message.
        - link: The link attached to the post.
        - name: The name of the link attachment.
        - picture: The URL of a picture attached to the post.
        - source: The URL of a media file (either SWF or MP3) attached
            to the post.
        - properties: A JSON object of key/value pairs which will appear in
            the stream attachment beneath the description, with each property
            on its own line.
        - ref: A text reference for the category of feed post.
        - to: The ID or username of the profile that this story will
            be published to.

    Please visit https://developers.facebook.com/docs/reference/dialogs/feed/
    for a detailed reference of the supported arguments by Facebook.
    """
    # Base javascript for the button.
    base_script = (
        "javascript:(function(){function post_to_facebook(){FB.ui({method:"
        "'feed',%(__KWARGS__)s});}window.fbAsyncInit=function(){FB.init({"
        "appId:'%(__APPID__)s',status:true,cookie:true,xfbml:true});"
        "FB.getLoginStatus(function(response){post_to_facebook();});};"
        "(function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];"
        "if(d.getElementById(id)){return;}js=d.createElement(s);js.id=id;"
        "js.src=('https:'==document.location.protocol?'https://':'http://')+"
        "'connect.facebook.net/en_US/all.js';"
        "fjs.parentNode.insertBefore(js,fjs);}"
        "(document,'script','facebook-jssdk'));"
        "if(typeof FB !== 'undefined'){post_to_facebook();}}());"
    )

    context['label'] = label or _('Share')
    context['css_class'] = css_class
    context['icon_class'] = icon_class
    context['script'] = base_script % {
        '__APPID__': APP_ID,
        '__KWARGS__': ','.join(["%s:'%s'" % i for i in kwargs.items()])
    }

    return template.loader.render_to_string(
        'facebook/share_button.html', context)
