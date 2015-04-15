django-socialnetworks
=====================

Initially this package was intended to provide "Log in with..."
capabilities to Django projects, but slowly as it was included in some
of my projects it has growth to be a simple but powerful API client for
some of the services that actually supports OAuth.

This package is built on top of the `Python Requests
library <http://docs.python-requests.org/>`__ and heavyly based/inspired
in `django-socialregistration
app <https://github.com/flashingpumpkin/django-socialregistration>`__
but with some improvements and needs required in my projects.

Installation
------------

.. code:: bash

    # Default installation
    $ pip install django-socialnetworks

    # Install security egg
    $ pip install django-socialnetworks[security]

Usage
-----

#. Add ``socialnetworks`` and the service's apps that you require to
   your ``INSTALLED_APPS``.

   .. code:: python

       # my_project/settings.py

       INSTALLED_APPS = (
           ...
           ...
           'socialnetworks',
           'socialnetworks.facebook',
           'socialnetworks.twitter'
           ...
           ...
       )

#. Set the ``SOCIALNETWORKS_CONFIGURATION`` dictionary.

   .. code:: python

       # my_project/settings.py

       SOCIALNETWORKS_CONFIGURATION = {
           'EMAIL_IS_USERNAME': False,
           'FACEBOOK': {
               'APP_ID': 'my-facebook-app-id',
               'APP_SECRET': 'my-facebook-app-secret',
               'SCOPE': ['first_name', 'last_name', 'username']
           },
           'TWITTER': {
               'APP_ID': 'my-twitter-app-id',
               'APP_SECRET': 'my-twitter-app-secret',
               'SCOPE': ['name', 'screen_name']
           },
       }

#. Add the allowed for login app backends to your
   ``AUTHENTICATION_BACKENDS``.

   .. code:: python

       # my_project/settings.py

       AUTHENTICATION_BACKENDS = (
           ...
           ...
           'socialnetworks.facebook.backends.FacebookBackend',
           'socialnetworks.twitter.backends.TwitterBackend',
           ...
           ...
       )

#. Add ``socialnetworks`` to your project urls.

   .. code:: python

       # my_project/urls.py

       urlpatterns = patterns('',
           ...
           ...
           url(r'^social/', include('socialnetworks.urls', namespace='socialnetwork')),
           ...
           ...
       )

#. Show ``Log in with...`` button in your templates.

   .. code:: html

       ...
       ...
       {% load facebook %}
       ...
       ...
       {% facebook_login 'Button text' 'css_class' %}
       ...
       ...

#. Request data from the service's API. Note that the clients **must be
   initialized** with the proper OAuth profile.

   .. code:: python

       from socialnetworks.facebook.clients import FacebookClient

       client = FacebookClient(user.facebookoauthprofile)
       data = client.get('me', params={'fields': 'first_name,last_name'})
       data['first_name']
       >>> 'John'

Available settings
------------------

Global:

-  ``COOKIE_MAX_AGE``: The max age of the cookies if you are storing
   social account data in cookies. Defaults to 900.
-  ``EMAIL_IS_USERNAME``: Tell whether the email is used as username in
   the site. Defaults to True.
-  ``ACTIVATE_ALREADY_REGISTERED_USERS``: Tell wheter to activate
   already registed but inactive users whose match a profile retrieved
   from the service's API. This is useful if you implement registration
   by sending an activation link and allow social login/registration at
   the same time. Defaults to False.
-  ``SETUP_TEMPLATE``: The name of the template used to render the setup
   view if needed.
-  ``SETUP_FORM_CLASS``: The name of the form class to be used to
   complete the setup process if needed.

App specific:

-  ``APP_ID``: The id of your app given by the service.
-  ``APP_SECRET``: The secret key of your app given by the service.
-  ``APP_ACCESS_TOKEN``: The access token of your app if required/given
   by the service (Facebook).
-  ``SCOPE``: A list of strings representing the scope of the tokens to
   be generated, you must check the available scopesprovided by the
   service you are using and it may require your app to be configured to
   request these scopes. By default it tries to request the email in the
   way it is provided specifically by each service.
-  ``SESSION_KEY``: The key to be used to store the relevant OAuth
   process data in the user's session. Defaults to 'dsn' + the
   representative letters of each service, ie, 'dsnfb', 'dsntw', etc.
-  ``SESSION_FIELDS``: The retrieved fields from the service's API that
   will be stored in the user's session if you are using cookies to
   store social account data.
-  ``SETUP_URL_NAME``: A custom url name for redirect the users to
   complete the account setup. This url name must be provided in the
   format 'namespace:url-name' since it will be resolved by using
   django.core.urlresolvers.reverse. This setting is useful if you want
   to complete the setup in an AJAX view. When the user is redirected to
   this url a 'dsnstp' cookie containing the user's data retrived from
   the service's API wit a max age of two minutes (120 seconds). Note
   that this cookie is a base64 encoded JSON dumped string.

Service specific:

-  PayPal:

   -  ``IS_LIVE``: Tell if your app is in live or sandbox mode to make
      the requests to the proper API endpoints.

Preload social account data in your views
=========================================

This is useful if you need to display data retrieved from the service's
API in your views, for example if you want to display the username and
profile picture of the current user in the service.

First you need to set the fields that will be retrieved from the service
and stored in a cookie (cookies are used to avoid the data not to be
updated if the user updates its profile in the service, cookies are by
default set to live for 15 minutes before a new requests to the
service's API is made).

.. code:: python

    # my_project/settings.py

    SOCIALNETWORKS_CONFIGURATION = {
        ...
        ...
        'FACEBOOK': {
            'APP_ID': 'my-facebook-app-id',
            'APP_SECRET': 'my-facebook-app-secret',
            'SCOPE': ['first_name', 'last_name', 'username'],
            'SESSION_FIELDS': ['username', 'picture.type(normal)']
        },
        ...
        ...
    }

**Note that since these methods make requests to the service's APIs is
highly probably that the applied views results in slower rendering or
timeout errors.**

.. code:: python

    # my_project/views.py

    from socialnetworks.facebook.decorators import fetch_facebook_data
    from socialnetworks.facebook.utils import read_facebook_data


    class MyDecoratedView(TemplateView):
        def get_context_data(self, **kwargs):
            context = super(MyDecoratedView, self).get_context_data(**kwargs)

            # Read the social data previously stored in a cookie and makes it
            # available in the view's context.
            context['facebook_data'] = read_facebook_data(self.request)

            return context

        # Prefetch the social data for the current authenticated user and store it
        # in a cookie.
        @method_decorator(fetch_facebook_data)
        def dispatch(self, request, *args, **kwargs):
            return super(MyDecoratedView, self).dispatch(request, *args, **kwargs)

Then render the retrieved data in the view's template.

.. code:: html

    ...
    ...
    <span>{{ facebook_data.username }}</span>
    <img src="{{ facebook_data.picture.data.url }}" />
    ...
    ...

Making requests to the service's APIs
-------------------------------------

First you need to initialize a client, then call the proper ``get`` or
``post`` method for the action you want to make passing the resource and
the parameters or the data tu retrive/put.

**Nothe that this is a work in progress, GET requests should work ok,
but POST must have some caveats depending on the service.**\ \*

.. code:: python

    from socialnetwork.facebook.clients import FacebookClient


    client = Facebook.client(user.facebookoauthprofile)

    # Retrieve data
    data = client.get('me', params={'fields': 'first_name', 'last_name'})
    print data
    >>> {'first_name': 'John', 'last_name': 'Smith'}

    # Post data
    client.post('me', data={'first_name': 'Juan'})
    data = client.get('me', params={'fields': 'first_name', 'last_name'})
    print data
    >>> {'first_name': 'Juan', 'last_name': 'Smith'}
