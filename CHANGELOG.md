# Changelog

## 0.4.11 (2015-06-18)

Bugfixes:

+ Fix django.core.exceptions.AppRegistryNotReady exception in Django >= 1.7


## 0.4.10 (2015-04-30)

Bugfixes:

+ Fixed bug not updating OAuth data in `MovesAppClient` instance after refreshing an access token.


## 0.4.9 (2015-04-24)

Bugfixes:

+ Fixed bug when calling `refresh_access_token` method of a `MovesOAuthProfile` instace.


## 0.4.8 (2015-04-15)

Features:

+ Added new 'security' extra egg that installs requests[security] as dependency.


## 0.4.7 (2014-11-28)

Features:

+ Updated Facebook client to perform requests to the grap API v2.2 endpoint.

Bugfixes:

+ Fixed identation error that was causing `unbound local error` on Twitter setup view.
+ Fixed error generating the auth params in the LinkedIn client.


## 0.4.6 (2014-11-14)

Features:

+ Changed __init__ method of clients to accept a custom OAuth authentication dictionary.
+ Added the headers parameter to get and post methods of clients to pass custom headers to requests.
+ Changes the auth_params parameter of get and post methods of clients to auth that can receive a custom authenticaton that will be passed to requests.


## 0.4.5 (2014-10-24)

Bugfixes:

+ Changed to_timestamp and from_timestamp method to return None if the parameter passed is None to fix issues with OAut v1 services.


## 0.4.4 (2014-09-18)

Bugfixes:

+ Fixed error in callback view that tries to serialize the token expiration datetime to JSON.
+ Fixed error in setup view returning None object as user when email are retrieved from the service API but without username.


## 0.4.3 (2014-09-18)

Bugfixes:

+ Fixed error in clients get en post methods that does not return a raw response if the request returns an http error code.


## 0.4.2 (2014-09-15)

Bugfixes:

+ Added shortcut imports in moves app.


## 0.4.1 (2014-09-11)

Bugfixes:

+ Fixed a bug that causes auth error with Facebook and Twitter.


## 0.4.0 (2014-09-11)

Features:

+ Added Moves app support https://dev.moves-app.com/
+ Added raw parameter to get and post client methods to return the raw requests response.
+ Added the posibility to handle refresh token requests (available in moves).

Bugfixes:

+ Refactorized OAuth access token flow to allow refresh tokens to be saved.


## 0.3.2 (2014-09-09)

Bugfixes:

+ Fixed bug that perfoms GET requests calling a client _post method.


## 0.3.1 (2014-09-08)

Features:

+ Added new ACTIVATE_ALREADY_REGISTERED_USERS option.

Bugfixes:

+ Fixed ImportError in templatetags relative imports.
+ Changed signal invocation to send view classes as sender parameter instead of view instances.


## 0.3.0 (2014-07-31)

Features:

+ Urls no longer care about user assigned namespaces.
+ Added support for a custom setup url for integration with AJAX views.
+ Generate suggested username is it was not provided by the service API .

Bugfixes:

+ Whole code clenaup and better PEP8 complaint.
+ Change all imports for relative imports.
+ Fixed the algorithm to link with an existing user or creating a new one.


## 0.2.0 (2014-07-07)

Features:

+ Added GitHub, Gravatar, LinkedIn and PayPal support
+ Higher max_length for storing service uids
+ Dropped Django < 1.5 support
+ Added created_date field for ouath profiles

Bugfixes:

+ Try to parse as JSON the access_token responses first


## 0.1.0 (unreleased)

Features:

+ Better client to make Facebook requests. Merged FacebookGraph into FacebookClient class
+ Rewrite of the base client code that adds better support for OAuth1 and OAuth2 services
+ Added support for Twitter (Sign in and share)
+ Better configuration options for settings
+ Support for custom template and form for the setup view

Bugfixes:

+ Removed all urllib based functions, now all the code makes use of requests and requests_oauthlib
+ Resolved broken translations
+ The javascript of the Facebook "Share" button is loaded inline



## 0.0.6 (2013-06-12)

Features:

+ Added templatetags for "Share" button with Facebook

Bugfiex:

+ Collision with django-socilregistration models


## 0.0.5 (2013-06-11)

Bugfixes:

+ Deprecated imports


## 0.0.4 (unreleased)

Features:

+ Added support for translations


## 0.0.3 (2013-06-05)

Features:

+ Better README
+ Better support for button styling


## 0.0.2 (2013-06-04)

Features:

+ Updated setup script

Bugfixes:

+ Template resolve problems


## 0.0.1 (2013-06-03)

Initial release

+ Support for "Sign in with Facebook"
