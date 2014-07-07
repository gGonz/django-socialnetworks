from django.conf.urls import url, patterns

from . import views


urlpatterns = patterns(
    '',
    url(r'^login/$',
        views.PayPalDialogRedirect.as_view(), name='login'),
    url(r'^callback/$',
        views.PayPalCallback.as_view(), name='callback'),
    url(r'^setup/$',
        views.PayPalSetup.as_view(), name='setup'),
    url(r'^disconnect/$',
        views.PayPalOAuthDisconnect.as_view(), name='disconnect'),
)
