from django.core.urlresolvers import reverse

from socialnetworks.base.views import (
    OAuthDialogRedirectView, OAuthCallbackView,
    OAuthSetupView, OAuthDisconnectView
)
from socialnetworks.twitter.clients import TwitterClient


class TwitterDialogRedirect(OAuthDialogRedirectView):
    client = TwitterClient()

    def get_callback_url(self):
        return self.client.get_domain() + reverse(
            'socialnetworks:twitter:callback')

    def get_redirect_url(self):
        return self.client.encode_url(self.client.authorization_url, {
            'oauth_token': self.session_get('request_token')})


class TwitterCallback(OAuthCallbackView):
    client = TwitterClient()

    def get_redirect_url(self):
        if self.session_get('new_user'):
            return reverse('socialnetworks:twitter:setup')

        else:
            return self.session_pop('next') or '/'


class TwitterSetupView(OAuthSetupView):
    client = TwitterClient()

    def get_redirect_url(self):
        return self.session_pop('next') or '/'

    def retrieve_user_data(self):
        # Retrieves the proper profile.
        profile = self.get_profile()

        # Creates a client that can make signed requests.
        tw = TwitterClient(profile)

        # Fetches the user's data from Twitter.
        data = tw.get(self.client.token_debug_url)

        # Parses the "name" of Twitter, simply splits the name by white
        # spaces, the first name is the first element of the resulting list,
        # the last name are the remaining elements joined again by white
        # spaces. If there are not white spaces in the name, then the first
        # name is the name returned by Twitter and the last name is
        # left blak.
        name = data['name']
        first_name = name.split(' ')[0] if ' ' in name else name
        last_name = ' '.join(name.split(' ')[1:]) if ' ' in name else None

        return {
            'first_name': first_name,
            'last_name': last_name,
        }


class TwitterOAuthDisconnect(OAuthDisconnectView):
    client = TwitterClient()
