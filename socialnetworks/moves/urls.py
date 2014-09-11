from django.conf.urls import url, patterns

from . import views


urlpatterns = patterns(
    '',
    url(r'^login/$',
        views.MovesAppDialogRedirect.as_view(), name='login'),
    url(r'^callback/$',
        views.MovesAppCallback.as_view(), name='callback'),
    url(r'^setup/$',
        views.MovesAppSetup.as_view(), name='setup'),
    url(r'^disconnect/$',
        views.MovesAppOAuthDisconnect.as_view(), name='disconnect'),
)
