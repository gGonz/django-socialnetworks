django-socialnetwork
====================

This packages provides login and share funcionalities for the social networks.

Installation
------------

.. code-block::

    pip install django-socialnetwork


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


3. Add the ``social backends`` to your ``AUTHENTICATION_BACKENDS``.

.. code-block:: python

    AUTHENTICATION_BACKENDS = (
        ...
        ...
        'socialnetwork.facebook.backends.FacebookBackend',
        ...
        ...
    )


4. Add ``socialnetwork`` to your ``urls``.

.. code-block:: python

    urlpatterns = patterns('',
        ...
        ...
        url(r'^social/', include('socialnetwork.urls', namespace='socialnetwork')),
        ...
        ...
    )

5. Show ``login button`` in your ``templates``.

.. code-block:: python

    ...
    ...
    {% load facebook %}
    ...
    ...
    {% facebook_login 'text to show in button' 'css_class1 css_class2 ... css_classN' %}
    ...
    ...

6. Share content using ``tags`` in your ``templates`` (you can provide any **named** args accepted by the Facebook JavaScript SDK).

.. code-block:: python
    
    ...
    ...
    {% load facebook %}
    ...
    ...
    {% facebook_share 'text to show in button' 'css_class1 css_class2 ... css_classN' link="mysite.com" name="This is my site" ... %}
    ...
    ...


7. Request data. The client **must be initialized** with a ``profile`` object.

.. code-block:: python

    ...
    ...
    from socialnetwork.facebook.clients import FacebookGraph
    ...
    ...
    graph = FacebookGraph(user.facebookoauthprofile)
    data = graph.get('me', params={'fields': 'first_name,last_name,picture.type(normal)'})
    data['first_name']
    >>> 'John'

8. Check access token.

.. code-block:: python

    graph.debug_access_token()
    >>> (True, {'data': {'is_valid':True, 'access_token':...}})


    

    


TODO
====

1. Provide a method to call a custom setup when the OAuth flow ends.
2. Extend support for OAuth 2 services (Foursquare, Github, etc.)
3. Add support for OAuth 1 services (Twitter, LinkedIn, etc.)