import json
import requests

from requests_oauthlib import OAuth1, OAuth2
from urlparse import parse_qsl

from django.contrib.auth import authenticate, login
from django.contrib.sites.models import Site


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

    def __init__(self, profile=None):
        self.profile = profile if profile else None

    def get_domain(self):
        """
        Returns the current site domain.

        """
        protocol = 'http://'
        return protocol + Site.objects.get_current().domain

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
        if self.profile:
            if self.oauth_version == 1:
                return {
                    'resource_owner_key': self.profile.oauth_access_token,
                    'resource_owner_secret': (
                        self.profile.oauth_access_token_secret),
                }

            elif self.oauth_version == 2:
                return {
                    'access_token': self.profile.oauth_access_token,
                    'token_type': 'bearer'
                }

        else:
            raise NameError('\'profile\' is not defined.')

    def compose_auth(self, auth_args={}):
        """
        Returns the auth header for the OAuth requests.

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

        """
        raise NotImplementedError

    def __request_get__(self, url, **kwargs):
        """
        Primitive to make a get request.

        """
        return requests.get(url, **kwargs)

    def __request_post__(self, url, data=None, **kwargs):
        """
        Primitive to make a post request.

        """
        return requests.get(url, data=data, **kwargs)

    def get(self, api_endpoint, params={}, auth_params=None):
        """
        Makes a get request to the service's API and returns the response
        in json format.

        Parameters:
            - api_endpoint: a string that defines the endpoint where the
                request will be directed, this will be concatenated with
                the base API url.
            - params: a dictionary containing all the extra parameters that
                will be passed to the API.
            - auth_params: a dictionary containing all the extra parameters
                needed to compose the OAuth auth header.

        """
        if self.profile and not auth_params:
            auth_params = self.get_auth_params()

        url = self.service_api_url + api_endpoint

        response = self.__request_get__(
            url, params=params,
            auth=self.compose_auth(auth_params)
        )

        return response.json()

    def post(self, api_endpoint, data=None, params={}, auth_params=None):
        """
        Makes a post request to the service's API and returns the response
        in json format.

        Parameters:
            - api_endpoint: a string that defines the endpoint where the
                request will be directed, this will be concatenated with
                the base API url.
            - data: the data that will be sent to the API in the POST body
                of the request.
            - params: a dictionary containing all the extra parameters that
                will be passed to the API.
            - auth_params: a dictionary containing all the extra parameters
                needed to compose the OAuth auth header.

        """
        if self.profile and not auth_params:
            auth_params = self.get_auth_params()

        url = self.service_api_url + api_endpoint

        response = self.__request_post__(
            url, data=data, params=params,
            auth=self.compose_auth(auth_params)
        )

        return response.json()


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
        r = self.__request_post__(
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
        r = self.__request_post__(self.access_token_url, auth=oauth)

        return self.parse_response(r.content)


class OAuth2Client(BaseOAuthClient):
    """
    Base client for OAuth2 services.

    """
    oauth_version = 2
    verifier_label = 'code'
    access_token_label = 'access_token'
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
        r = self.__request_post__(self.access_token_url, params=params)

        return self.parse_response(r.content)
