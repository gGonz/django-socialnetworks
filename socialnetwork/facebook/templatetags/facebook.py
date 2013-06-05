from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

register = template.Library()


@register.simple_tag(takes_context=True)
def facebook_login(context, text=None, css_class=None):

    context['value'] = text or _('Sign in with Facebook')
    context['action'] = reverse('socialnetwork:facebook:login')
    context['css_class'] = css_class

    return template.loader.render_to_string(
        'login/login_button.html', context
    )
