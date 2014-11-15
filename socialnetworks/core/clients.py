import json
import requests

from requests_oauthlib import OAuth1, OAuth2
from urlparse import parse_qsl

from django.contrib.auth import authenticate, login

from .models import BaseSocialProfile


class BaseOAuthClient(object):
    """
    Base class that defines the client for OAuth services.
    """
    # The version of the OAuth protocol used by the client.
    oauth_version = None

    # The name of the service.
    service_name = None

    # The app's client id provided by the service.
    app_key = None

    # The app's secret provided by the service.
    app_secret = None

    # The app's access token provided by the service.
    app_access_token = None

    # The base url for make requests to the service API.
    service_api_url = None

    # The url where the service give us the request token.
    request_token_url = None

    # The url where the service shows the auth/login dialog to the user.
    authorization_url = None

    # The url where the service give us the access token.
    access_token_url = None

    # The label of the request token in the service.
    request_token_label = None

    # The label of the request token secret in the service.
    request_token_secret_label = None

    # The label of the access token in the service.
    access_token_label = None

    # The label of the access token secret in the service.
    access_token_secret_label = None

    # The label of the refresh token in the service if available.
    refresh_token_label = None

    # The label of the user's id in the service.
    uid_label = None

    # The label of the access token expiration in the service.
    expiration_label = None

    # The url where the access token can be debbuged.
    token_debug_url = None

    # The key for the session dictionary where the flow data will be stored.
    session_key = None

    # The label that is used by the service to name its OAuth verifier.
    verifier_label = 'None'

    # The permissions that the app will ask for.
    scope = None

    # The model where the profiles are stored.
    model = None

    def __init__(self, profile=None, oauth_data=None):
        """
        Initialize a client instance storing the OAuth authentication data in
        the '_oauth_data' dictionary.

        Pass only one of 'profile' or 'oauth_parameters' to initialize the
        client, if both are provided 'profile' takes precedence
        over 'oauth_data'.

        Note that if the instance is initialized with a valid instance of the
        model defined in 'model' property it will be stored in the '_profile'
        property, otherwise this property will be set to None.

        If the instance is iniatilized passing a dict instance as the
        'oauth_data' parameter it must be at least contain the 'access_token'
        key that is required for OAuth v2 authentication. If the client
        performs requests to an OAuth v1 service the 'oauth_data' must also
        contain the 'token_secret' key othwewise the client will fail to
        build the authentication parameters.
        """
        if profile is not None:
            if isinstance(profile, BaseSocialProfile):
                self._oauth_data = {
                    'access_token': getattr(
                        profile, 'oauth_access_token'),
                    'token_secret': getattr(
                        profile, 'oauth_access_token_secret', None),
                    'refresh_token': getattr(
                        profile, 'oauth_refresh_token', None),
                    'expiration': getattr(
                        profile, 'oauth_access_token_expires_at', None)
                }

                self._profile = profile

            else:
                raise ValueError(
                    "'profile' parameter must be a '%s' model instance" %
                    self.model.__name__
                )

        elif oauth_data:
            if isinstance(oauth_data, dict):
                self._oauth_data = {
                    'access_token': oauth_data.get('access_token'),
                    'token_secret': oauth_data.get('token_secret', None),
                    'refresh_token': oauth_data.get('refresh_token', None),
                    'expiration': oauth_data.get('expiration', None)
                }

            else:
                raise ValueError(
                    "'oauth_data' parameter must be a dict instance")

    def _get(self, url, **kwargs):
        """
        Base method to perform GET requests by wrapping the
        'requests' python library.
        """
        return requests.get(url, **kwargs)

    def _post(self, url, data=None, **kwargs):
        """
        Base method to perform POST requests by wrapping the
        'requests' python library.
        """
        return requests.post(url, data=data, **kwargs)

    def encode_url(self, url, params={}):
        """
        Returns the encoded url with thw given parameters.
        """
        try:
            r = requests.Request(url=url, params=params).prepare()
            return r.url

        except:
            encoder = requests.models.RequestEncodingMixin()
            enc_params = encoder._encode_params(params)
            return url + '?' + enc_params

    def login(self, request, uid):
        """
        Logs the user in.
        """
        login(request, authenticate(**{'service_uid': uid}))

    def parse_response(self, data):
        """
        Returns a dictionary of the parsed response.
        """
        try:
            return json.loads(data)

        except:
            return dict(parse_qsl(data))

    def get_auth_params(self):
        """
        Returns a dictionary containing the proper parameters to compose
        the OAuth auth header.
        """
        if self.oauth_version == 1:
            return {
                'resource_owner_key': self._oauth_data['access_token'],
                'resource_owner_secret': self._oauth_data['token_secret']
            }

        elif self.oauth_version == 2:
            return {
                'access_token': self._oauth_data['access_token'],
                'token_type': 'bearer'
            }

    def compose_auth(self, auth_args={}):
        """
        Returns the auth header for the OAuth requests.

        Subclasses must implement this method.
        """
        raise NotImplementedError

    def compose_authorization_url(self, callback_url):
        """
        Return the url where the user should be redirected to request
        authorization for its account details.

        Subclasses must implement this method.
        """
        raise NotImplementedError

    def get_request_token(self):
        """
        Connects with the service to obtain the OAuth request token and
        returns a dictionary with the parsed token.

        OAuth1 subclasses must implement this method.
        """
        raise NotImplementedError

    def get_access_token(self):
        """
        Connects with the service to obtain the OAuth access token and
        returns a dictionary with the parsed token.

        Subclasses must implement this method.
        """
        raise NotImplementedError

    def debug_access_token(self):
        """
        Connects with the service to check if the access token is valid and
        returns a tuple where the first element is a boolean indicating the
        validity and the second is the response from the service.

        Subclasses must implement this method.
        """
        raise NotImplementedError

    def refresh_access_token(self, profile=None, update=True):
        """
        Connects with the service to request a new access token for the
        given profile.

        Pass update=True to force the given profile to be updated with the
        retrieved data.

        Subclasses must implement this method.
        """
        raise NotImplementedError

    def retrieve_user_data(self, profile=None):
        """
        Return the available user data that can be retrieved from the
        service's API in a python/django friendly format.

        Subclasses must implement this method.
        """
        raise NotImplementedError

    def get(self, endpoint, params={}, headers={}, auth=None, raw=False):
        """
        Makes a get request to the service's API and returns the response
        in json format.

        Parameters:
            - endpoint: a string that defines the endpoint where the
                request will be directed, this will be concatenated with
                the base API url.

            - params: a dictionary containing all the extra get parameters
                (querystring) that will be passed to the service's API in
                the request.

            - headers: a dictionary containing all the extra headers that will
                be passed to the service's API in the request.

            - auth: a custom OAuth authentication object to replace the
                calculated authentication.

            - raw: a boolean that tells if the method should return the raw
                requests module response when True or the parsed JSON
                response data.
        """
        url = self.service_api_url + endpoint
        auth = (auth if auth is not None else
                self.compose_auth(self.get_auth_params()))

        response = self._get(url, params=params, headers=headers, auth=auth)

        return response if raw else response.json()

    def post(self, endpoint, data=None, params={}, headers={},
             auth=None, raw=False):
        """
        Makes a post request to the service's API and returns the response
        in json format.

        Parameters:
            - endpoint: a string that defines the endpoint where the
                request will be directed, this will be concatenated with
                the base API url.

            - data: the data that will be sent to the API in the POST body
                of the request.

            - params: a dictionary containing all the extra get parameters
                (querystring) that will be passed to the service's API in
                the request.

            - headers: a dictionary containing all the extra headers that will
                be passed to the service's API in the request.

            - auth: a custom OAuth authentication object to replace the
                calculated authentication.

            - raw: a boolean that tells if the method should return the raw
                requests module response when True or the parsed JSON
                response data.
        """
        url = self.service_api_url + endpoint
        auth = (auth if auth is not None else
                self.compose_auth(self.get_auth_params()))

        response = self._post(url, data=data, params=params, headers=headers,
                              auth=auth)

        return response if raw else response.json()


class OAuth1Client(BaseOAuthClient):
    """
    Base client for OAuth1 services.
    """
    oauth_version = 1
    verifier_label = 'oauth_verifier'
    request_token_label = 'oauth_token'
    request_token_secret_label = 'oauth_token_secret'
    access_token_label = 'oauth_token'
    access_token_secret_label = 'oauth_token_secret'
    uid_label = 'user_id'

    def compose_auth(self, auth_params={}):
        auth_params.update({'client_secret': self.app_secret})

        return OAuth1(self.app_key, **auth_params)

    def get_request_token(self, callback=None):
        # Gets the authentication header.
        oauth = self.compose_auth()

        # Requesting and parsing the request token.
        r = self._post(
            self.request_token_url, auth=oauth,
            params={'oauth_callback': callback}
        )

        return self.parse_response(r.content)

    def get_access_token(self, request_token=None,
                         request_token_secret=None, verifier=None):
        # Gets the authentication header.
        oauth = self.compose_auth({
            'resource_owner_key': request_token,
            'resource_owner_secret': request_token_secret,
            'verifier': verifier
        })

        # Requesting and parsing the access token.
        r = self._post(self.access_token_url, auth=oauth)

        return self.parse_response(r.content)


class OAuth2Client(BaseOAuthClient):
    """
    Base client for OAuth2 services.
    """
    oauth_version = 2
    verifier_label = 'code'
    access_token_label = 'access_token'
    refresh_token_label = 'refresh_token'
    uid_label = 'user_id'

    def compose_auth(self, auth_params={}):
        return OAuth2(client_id=self.app_key, token=auth_params)

    def get_access_token(self, verifier=None, callback=None):
        # Composes the parameters for the request.
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.app_key,
            'client_secret': self.app_secret,
            'redirect_uri': callback,
            self.verifier_label: verifier
        }

        # Requesting and parsing the access token.
        r = self._post(self.access_token_url, params=params)

        return self.parse_response(r.content)
