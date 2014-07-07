# Changelog

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
