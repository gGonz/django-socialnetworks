import urllib

from django.core.urlresolvers import reverse

from socialnetwork.base.views import (
    OAuthDialogRedirectView, OAuthCallbackView,
    OAuthSetupView, BaseProfileDisconnectView
)
from socialnetwork.facebook.clients import FacebookClient, FacebookGraph


class FacebookDialogRedirect(OAuthDialogRedirectView):
    client = FacebookClient()

    def get_redirect_url(self):
        return '%(url)s%(params)s' % {
            'url': self.client.login_dialog_endpoint,
            'params': urllib.urlencode({
                'client_id': self.client.client_id,
                'redirect_uri': self.client.get_callback_url(),
                'scope': self.client.scope,
            })
        }


class FacebookCallback(OAuthCallbackView):
    client = FacebookClient()

    def get_redirect_url(self):
        if self.session_get('new_user'):
            return reverse('socialnetwork:facebook:setup')

        else:
            redirect_url = self.session_get('next')
            self.session_clear()
            return redirect_url or '/'


class FacebookSetup(OAuthSetupView):
    client = FacebookClient()

    def get_redirect_url(self):
        redirect_url = self.session_get('next')
        self.session_clear()
        return redirect_url or '/'

    def retrieve_user_data(self):
        graph = FacebookGraph(
            self.client.model.objects.get(
                service_uid=self.session_get('uid')
            )
        )

        fields = ['first_name', 'last_name', 'email', 'username']

        data = graph.get('me', params={'fields': ','.join(fields)})

        if self.client.email_is_username:
            data['username'] = data['email']

        return dict(zip(fields, [data[f] for f in fields]))


class FacebookProfileDisconnect(BaseProfileDisconnectView):
    client = FacebookClient()

    def get_profile(self):
        try:
            return self.request.user.facebookprofile
        except:
            return None
