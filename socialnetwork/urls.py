from django.conf.urls import url, patterns, include


urlpatterns = patterns('',
    url(
        r'^facebook/',
        include('socialnetwork.facebook.urls', namespace='facebook')
    ),
)
