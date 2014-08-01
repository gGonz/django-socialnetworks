from django.conf.urls import url, patterns

from . import views


urlpatterns = patterns(
    '',
    url(r'^login/$',
        views.FacebookDialogRedirect.as_view(), name='login'),
    url(r'^callback/$',
        views.FacebookCallback.as_view(), name='callback'),
    url(r'^setup/$',
        views.FacebookSetup.as_view(), name='setup'),
    url(r'^disconnect/$',
        views.FacebookOAuthDisconnect.as_view(), name='disconnect'),
)
