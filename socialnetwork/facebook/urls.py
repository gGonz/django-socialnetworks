from django.conf.urls import url, patterns

from socialnetwork.facebook import views


urlpatterns = patterns('',
    url(
        r'^login/$',
        views.FacebookDialogRedirect.as_view(), name='login'
    ),
    url(
        r'^callback/$',
        views.FacebookCallback.as_view(), name='callback'
    ),
    url(
        r'^setup/$',
        views.FacebookSetup.as_view(), name='setup'
    ),
    url(
        r'^disconnect/$',
        views.FacebookOAuthProfileDisconnect.as_view(), name='disconnect'
    ),
)
