from django.conf.urls import url, patterns

from . import views


urlpatterns = patterns(
    '',
    url(r'^login/$',
        views.GitHubDialogRedirect.as_view(), name='login'),
    url(r'^callback/$',
        views.GitHubCallback.as_view(), name='callback'),
    url(r'^setup/$',
        views.GitHubSetup.as_view(), name='setup'),
    url(r'^disconnect/$',
        views.GitHubOAuthDisconnect.as_view(), name='disconnect'),
)
