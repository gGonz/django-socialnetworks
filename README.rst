django-socialnetwork
====================

This packages provides login and share funcionalities for the social networks.

Installation
------------

.. code-block::

    pip install django-socialregistration


Basic usage
-----------

1. Add ``socialnetwork`` to ``INSTALLED_APPS``.

.. code-block:: python

    INSTALLED_APPS = (
        ...
        ...
        'socialnetwork',
        'socialnetwork.facebook',
        ...
        ...
    )

2. Set your ``social app`` configuration in ``settings``.

.. code-block:: python

    SOCIALNETWORK_FACEBOOK_CLIENT_ID = '0123456789'
    SOCIALNETWORK_FACEBOOK_CLIENT_SECRET = '0123456789abcdefgh'
    SOCIALNETWORK_FACEBOOK_SCOPE_PERMISSIONS = ['email', ...]


3. Add ``socialnetwork`` to your ``urls``.

.. code-block:: python

    urlpatterns = patterns('',
        ...
        ...
        url(r'^social/', include('socialnetwork.urls', namespace='socialnetwork')),
        ...
        ...
    )

4. Show ``login button`` in your ``templates``.

.. code-block:: python

    ...
    ...
    {% load facebook %}
    ...
    ...
    {% facebook_login 'text to show in button' 'css_class1 css_class2 ... css_classN' %}
    ...
    ...

5. Request data. The client **must be initialized** with a ``profile`` object.

.. code-block:: python

    ...
    ...
    from socialnetwork.facebook.clients import FacebookGraph
    ...
    ...
    graph = FacebookGraph(user.facebookprofile)
    data = graph.get('me', params={'fields': 'first_name,last_name,picture.type(normal)'})
    data['first_name']
    >>> 'John'

6. Check access token.

.. code-block:: python

    graph.debug_access_token()
    >>> (True, {'data': {'is_valid':True, 'access_token':...}})


TODO
====

1. Add support for ``share button``.
2. Extend support for OAuth 2 services (Foursquare, Github, etc.)
3. Add support for OAuth 1 services (Twitter, LinkedIn, etc.)