from django.conf import settings
from django.conf.urls import url, patterns, include


urlpatterns = patterns('',)

if 'socialnetworks.facebook' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^facebook/',
            include('socialnetworks.facebook.urls', namespace='facebook')
        ),
    )

if 'socialnetworks.twitter' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^twitter/',
            include('socialnetworks.twitter.urls', namespace='twitter')
        ),
    )
