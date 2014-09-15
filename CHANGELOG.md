# Changelog

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
