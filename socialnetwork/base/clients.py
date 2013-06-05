import requests
import urlparse

from django.contrib.auth import authenticate, login


class BaseOAuth2Client(object):
    """
    Base class that defines the client for OAuth2 services.

    """
    # The name of the service.
    service_name = None

    # The app's client id provided by the service.
    client_id = None

    # The app's secret provided by the service.
    client_secret = None

    # The app's access token provided by the service.
    app_access_token = None

    # The endpoint of the service's api where the auth/login
    # dialog is requested.
    login_dialog_endpoint = None

    # The endpoint of the service's api where the access token is requested.
    access_token_endpoint = None

    # The permissions that the app will ask for.
    scope = None

    # Is the email used as username in the site?
    email_is_username = None

    # The model where the profiles are stored.
    model = None

    # The key for the session dictionary where the flow data will be stored.
    session_key = None

    def login(self, request, uid):
        """
        Logs the user in.

        """
        login(request, authenticate(**{'service_uid': uid}))

    def get_callback_url(self):
        """
        Returns the absolute url that will be passed as callback argument
        for the OAuth login/auth dialog.

        Subclasses must implement this method.

        """
        raise NotImplementedError

    def request_access_token(self, code, method='GET'):
        """
        Requests the access token to the service provider. If the access
        token is valid, stores it in the current user's session.

        """
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.get_callback_url(),
            'code': code
        }

        if method.upper() == 'GET':
            response = requests.get(
                self.access_token_endpoint, params=params
            )

        elif method.upper() == 'POST':
            response = requests.post(
                self.access_token_endpoint, params=params
            )

        return self.parse_access_token(
            response.content
        ).get('access_token', None)

    def parse_access_token(self, content):
        """
        Parses the query string returned by the service as the response of
        the access token request.

        """
        return dict(urlparse.parse_qsl(content))

    def debug_access_token(self):
        """
        Checks if the given access token is valid.

        Should update the access_token_expires_at, and uid atrributes.
        Should return a boolean.

        """
        raise NotImplementedError

    def request(
        self, endpoint, method='GET', params={}, headers={}, signature=None):
        """
        Makes a request against an api endpoint. If the request needs to be
        signed, the signature is required to be a dictionary.

        """
        if signature:
            params.update(signature)

        if method.upper() == 'GET':
            response = requests.get(
                endpoint,
                params=params
            )

        elif method.upper() == 'POST':
            response = requests.post(
                endpoint,
                params=params, headers=headers
            )

        return response.json()
