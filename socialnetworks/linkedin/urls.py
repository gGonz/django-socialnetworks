from django.conf.urls import url, patterns

from . import views


urlpatterns = patterns(
    '',
    url(r'^login/$',
        views.LinkedInDialogRedirect.as_view(), name='login'),
    url(r'^callback/$',
        views.LinkedInCallback.as_view(), name='callback'),
    url(r'^setup/$',
        views.LinkedInSetup.as_view(), name='setup'),
    url(r'^disconnect/$',
        views.LinkedInOAuthDisconnect.as_view(), name='disconnect'),
)
