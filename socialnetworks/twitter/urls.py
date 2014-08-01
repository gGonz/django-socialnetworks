from django.conf.urls import url, patterns

from . import views


urlpatterns = patterns(
    '',
    url(r'^login/$',
        views.TwitterDialogRedirect.as_view(), name='login'),
    url(r'^callback/$',
        views.TwitterCallback.as_view(), name='callback'),
    url(r'^setup/$',
        views.TwitterSetupView.as_view(), name='setup'),
    url(r'^disconnect/$',
        views.TwitterOAuthDisconnect.as_view(), name='disconnect'),
)
