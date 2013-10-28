from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


register = template.Library()


@register.simple_tag(takes_context=True)
def github_login(context, label=None, css_class=None, icon_class=None):
    """
    Renders a 'Sign in with GitHub' button.

    """
    context['label'] = label or _('Sign in with GitHub')
    context['action'] = reverse('socialnetworks:github:login')
    context['css_class'] = css_class
    context['icon_class'] = icon_class

    return template.loader.render_to_string(
        'github/login_button.html', context)
