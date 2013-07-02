from django.conf import settings
from django.conf.urls import url, patterns, include


urlpatterns = patterns('',)

if 'socialnetwork.facebook' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^facebook/',
            include('socialnetwork.facebook.urls', namespace='facebook')
        ),
    )

if 'socialnetwork.twitter' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^twitter/',
            include('socialnetwork.twitter.urls', namespace='twitter')
        ),
    )
