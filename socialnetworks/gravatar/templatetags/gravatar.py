from hashlib import md5
from urllib import urlencode

from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def gravatar(context, user=None, email=None, gid=None, size=40, default=''):
    """
    Retrieves the gravatar url from a given user, email or hash.
    """
    gravatar_url = 'http://www.gravatar.com/avatar/'

    if ('user' in context and context['user'].is_authenticated() and
            not (user or email or gid)):
        _hash = md5(context['user'].email).hexdigest()

    elif user and not (email or gid):
        _hash = md5(user.email).hexdigest()

    elif email and not gid:
        _hash = md5(email).hexdigest()

    elif gid:
        _hash = gid

    else:
        _hash = None

    if _hash:
        return gravatar_url + _hash + '?' + urlencode(
            {'d': default, 's': size})

    return ''
