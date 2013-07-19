from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from socialnetworks.facebook.settings import APP_ID


register = template.Library()


@register.simple_tag(takes_context=True)
def facebook_login(context, label=None, css_class=None):
    """
    Renders a 'Sign in with Facebook' button.

    """
    context['label'] = label or _('Sign in with Facebook')
    context['action'] = reverse('socialnetworks:facebook:login')
    context['css_class'] = css_class

    return template.loader.render_to_string('login_button.html', context)


@register.simple_tag(takes_context=True)
def facebook_share(context, label=None, css_class=None, **kwargs):
    """
    Renders a 'Share' button to share content on Facebook.

    Parameters:
        - label: the text to show inside the button, default 'Tweet'
        - css_class: the class to apply to the button

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
    context['script'] = base_script % {
        '__APPID__': APP_ID,
        '__KWARGS__': ','.join(["%s:'%s'" % i for i in kwargs.items()])
    }

    return template.loader.render_to_string('share_button.html', context)
