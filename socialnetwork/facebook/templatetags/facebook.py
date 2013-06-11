from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from socialnetwork.facebook.settings import CLIENT_ID

register = template.Library()


@register.simple_tag(takes_context=True)
def facebook_login(context, text=None, css_class=None):

    context['value'] = text or _('Sign in with Facebook')
    context['action'] = reverse('socialnetwork:facebook:login')
    context['css_class'] = css_class

    return template.loader.render_to_string(
        'login/login_button.html', context
    )


@register.simple_tag(takes_context=True)
def facebook_share(context, text=None, css_class=None, **kwargs):

    context['value'] = text or _('Share in Facebook')
    context['css_class'] = css_class
    context['client_id'] = CLIENT_ID
    context['onclick'] = ("FB.ui({method:'feed',%s})" %
        ','.join(["%s:'%s'" % i for i in kwargs.items()])
    )

    return template.loader.render_to_string(
        'share/share_button.html', context
    )
