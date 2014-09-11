from django.conf import settings
from django.conf.urls import url, patterns, include


urlpatterns = patterns('',)


if 'socialnetworks.facebook' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns(
        '',
        url(r'^facebook/',
            include('socialnetworks.facebook.urls', namespace='facebook')),
    )


if 'socialnetworks.github' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns(
        '',
        url(r'^github/',
            include('socialnetworks.github.urls', namespace='github')),
    )


if 'socialnetworks.linkedin' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns(
        '',
        url(r'^linkedin/',
            include('socialnetworks.linkedin.urls', namespace='linkedin')),
    )


if 'socialnetworks.moves' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns(
        '',
        url(r'^moves-app/',
            include('socialnetworks.moves.urls', namespace='moves-app')),
    )


if 'socialnetworks.paypal' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns(
        '',
        url(r'^paypal/',
            include('socialnetworks.paypal.urls', namespace='paypal')),
    )


if 'socialnetworks.twitter' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns(
        '',
        url(r'^twitter/',
            include('socialnetworks.twitter.urls', namespace='twitter')),
    )
