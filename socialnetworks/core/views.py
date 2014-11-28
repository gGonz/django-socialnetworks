import json

from base64 import b64encode
from datetime import timedelta
from urlparse import urlparse, parse_qs

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View, TemplateView

from . import settings
from .utils import compose_username, from_timestamp, to_timestamp
from ..signals import activation, connect, disconnect, login


class OAuthMixin(object):
    """
    Mixin that defines the necessary methods for OAuth views.
    OAuth views must be inherited from this class.
    """
    # The client class that defines the necessary information to perform
    # the OAuth flow.
    client_class = None

    def __init__(self, *args, **kwargs):
        super(OAuthMixin, self).__init__(*args, **kwargs)

        if self.client_class is not None:
            self.client = self.client_class()

        else:
            raise ImproperlyConfigured(
                "A valid client_class must be specified to initialize a "
                "'%s' view." % self.__class__
            )

    def _build_absolute_uri(self, uri):
        """
        Compose and return the fully qualified url for the given uri by
        wrapping the build_abosulte_uri method of the current request..
        """
        return self.request.build_absolute_uri(uri)

    def _get_session(self):
        """
        Returns the current session's object to store the data that will
        be used trough the OAuth flow.
        """
        if self.client.session_key not in self.request.session:
            self.request.session[self.client.session_key] = {}

        return self.request.session[self.client.session_key]

    def _set_session(self, dictionary):
        """
        Updates the current session's object, useful if the backend is not
        configured to save session in every request.
        """
        self.request.session[self.client.session_key] = dictionary

    def _get_namespace(self):
        """
        Return the namespace of the current path to build uris without
        worrying about user assignaed url namespaces.
        """
        return resolve(self.request.path).namespace

    def _prepend_namespace(self, url_name):
        """
        Return the given url name prepended with the current namespace.
        Must be used only for build url names that take care about namespace.
        """
        return ':'.join((self._get_namespace(), url_name))

    def session_get(self, key):
        """
        Returns the provided key value from the current session's object. If
        key is not in the object returns None.
        """
        return self._get_session().get(key, None)

    def session_put(self, **dictionary):
        """
        Puts the given dictionary into the current session's object.
        """
        session = self._get_session()
        session.update(**dictionary)
        self._set_session(session)

    def session_pop(self, key):
        """
        Returns the provided key value from the current session's object and
        removes the key from the object. If key is not in the object returns
        None.
        """
        session = self._get_session()
        value = session.pop(key, None)
        self._set_session(session)

        return value

    def session_clear(self):
        """
        Removes the object where the flow information of the service are
        stored from the current user's session.
        """
        if self.client.session_key in self.request.session:
            del self.request.session[self.client.session_key]

    def get_callback_url(self):
        """
        Return the callback url for the current request and service.
        """
        url_name = self._prepend_namespace('callback')
        url = reverse(url_name)

        return self._build_absolute_uri(url)

    def get_redirect_url(self):
        """
        Returns the url where the user will be redirected after its request
        is processed and is successfully logged in.
        """
        raise NotImplementedError

    def get_profile(self):
        """
        Returns the current user's OAuth profile or None.
        """
        raise NotImplementedError

    def create_new_user(self, data):
        """
        Returns a new user, created from the data dictionary.
        """
        raise NotImplementedError


class OAuthDialogRedirectView(OAuthMixin, View):
    """
    Base view that handles the redirection to the service
    authorization dialog.
    """
    def post(self, request, *args, **kwargs):
        # Clears the current session to avoid conflicts.
        self.session_clear()

        # Fetches the url where the user will be redirected when the
        # flow ends and stores it in the user's session.
        if 'next' in request.POST:
            self.session_put(**{'next': request.POST['next']})

        else:
            self.session_put(**{'next': '/'})

        if 'only_login' in request.POST:
            self.session_put(**{'only_login': request.POST['only_login']})

        if self.client.oauth_version == 1:
            # Gets the OAuth request token.
            credentials = self.client.get_request_token(
                callback=self.get_callback_url())

            request_token = credentials.get(self.client.request_token_label)
            request_token_secret = credentials.get(
                self.client.request_token_secret_label)

            # Appends the response to the user session.
            self.session_put(**{
                'oauth_request_token': request_token,
                'oauth_request_token_secret': request_token_secret
            })

        # Redirects the user to the authorization dialog.
        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        """
        Returns the url where the user should be redirected to request
        autorization to its account details.
        """
        if self.client.oauth_version == 1:
            param = self.session_get('oauth_request_token')

        elif self.client.oauth_version == 2:
            param = self.get_callback_url()

        return self.client.compose_authorization_url(param)


class OAuthCallbackView(OAuthMixin, View):
    """
    Base view that handles the callback redirection from the service.
    """
    def get(self, request, *args, **kwargs):
        # Protects the view to be accessed by non OAuth requests.
        if self.client.verifier_label not in request.GET:
            return HttpResponseForbidden()

        request_token = self.session_get('oauth_request_token')
        request_token_secret = self.session_get('oauth_request_token_secret')

        # Gets the OAuth access token.
        if self.client.oauth_version == 1:
            credentials = self.client.get_access_token(
                request_token=request_token,
                request_token_secret=request_token_secret,
                verifier=request.GET[self.client.verifier_label]
            )

        elif self.client.oauth_version == 2:
            credentials = self.client.get_access_token(
                verifier=request.GET[self.client.verifier_label],
                callback=self.get_callback_url(),
            )

        # Verifies if the service's user id was provided in the credentials,
        # if it was not provided then fetches it by debugging the access token.
        service_uid = credentials.get(self.client.uid_label, None)
        access_token = credentials.get(self.client.access_token_label, None)
        refresh_token = credentials.get(self.client.refresh_token_label, None)
        token_expiration = credentials.get(self.client.expiration_label, None)
        access_token_secret = credentials.get(
            self.client.access_token_secret_label, None)

        # Calculates the token expiration date.
        if token_expiration is not None:
            token_expiration = (
                timezone.now() + timedelta(seconds=int(token_expiration)))

        # Debugs the token.
        if service_uid is None:
            is_valid, debugged_data = self.client.debug_access_token(
                access_token)

            if is_valid:
                service_uid = debugged_data.get(self.client.uid_label)

        # Appends the response to the user session.
        profile_data = {
            'service_uid': service_uid,
            'oauth_access_token': access_token,
            'oauth_access_token_secret': access_token_secret,
            'oauth_access_token_expires_at': to_timestamp(token_expiration),
            'oauth_request_token': request_token,
            'oauth_request_token_secret': request_token_secret,
            'oauth_refresh_token': refresh_token
        }

        self.session_put(**profile_data)

        # Gets the lookups to retrieve or create the profile.
        lookup_kwargs = {'service_uid': service_uid}

        # Tries to retrieve the profile.
        try:
            profile = self.client.model.objects.get(**lookup_kwargs)
            created = False

        except self.client.model.DoesNotExist:
            profile = None

        # If there is no profile and the button clicked was only login
        # redirects the user to the page where it comes from, otherwise
        # creates a new profile with the given data.
        if not profile:
            if self.session_get('only_login'):
                parsed = urlparse(self.session_pop('only_login'))
                params = parse_qs(parsed.query)
                params.update(oauth_error=True)

                return redirect(self.client.encode_url(parsed.path, params))

            else:
                profile = self.client.model.objects.create(**lookup_kwargs)
                created = True

        # Reconvert the token expiration to a Python datetime object.
        profile_data.update(oauth_access_token_expires_at=from_timestamp(
            profile_data['oauth_access_token_expires_at']))

        # Updates the profile to make sure that we have always the most
        # recent token.
        profile.__dict__.update(**profile_data)
        profile.save()

        # If the profile was created or has no user then tries to attach the
        # profile to current user, if the user is not logged in then redirects
        # it to the final setup view to create a new user instance prefilled
        # with the data retrieved from the service's API.
        if created or not profile.user:
            if request.user.is_authenticated():
                profile.user = request.user
                profile.save()

                # Tells to the site that the user has connected its profile.
                connect.send(
                    sender=self.__class__, user=request.user,
                    service=self.client.service_name.lower()
                )

                # Tells to the user that his connection was successful.
                tags = 'social %s' % self.client.service_name.lower()
                messages.success(request, _(
                    'Your %(service)s profile was successfully connected '
                    'with your user account.'
                ) % {'service': self.client.service_name}, extra_tags=tags)

            else:
                self.session_put(**{'new_user': True})

        elif (profile.user and profile.user != request.user and
                request.user.is_authenticated()):

            # Tells to the user that his connection was unsuccessful.
            tags = 'social %s' % self.client.service_name.lower()
            messages.error(request, _(
                'This %(service)s profile is already connected with another '
                'user account.'
            ) % {'service': self.client.service_name}, extra_tags=tags)

        else:
            if not request.user.is_authenticated():
                # Logs the user in if it is not logged in yet.
                self.client.login(request, self.session_get('service_uid'))

                # Tells to the site that the user was logged in.
                login.send(
                    sender=self.__class__, user=request.user,
                    service=self.client.service_name.lower()
                )

            # Tells to the site that the user has connected its profile.
            connect.send(
                sender=self.__class__, user=request.user,
                service=self.client.service_name.lower()
            )

        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        """
        Return the url to redirect the user after processing the
        current request.
        """
        if self.session_get('new_user') is not None:
            url_name = self._prepend_namespace('setup')
            url = reverse(url_name)

        else:
            url = self.session_pop('next') or '/'

        return self._build_absolute_uri(url)


class OAuthSetupView(OAuthMixin, TemplateView):
    """
    Base View that handles the setup for the account after the access
    token is provided.
    """
    template_name = settings.SETUP_TEMPLATE
    setup_url = None

    def get_profile(self):
        """
        Tries to return the OAuth profile by retrieving the service_uid
        in the current session.
        """
        try:
            return self.client.model.objects.get(
                service_uid=self.session_get('service_uid'))

        except self.client.model.DoesNotExist:
            return None

    def create_new_user(self, data):
        """
        Create and return a new user with the given data.
        """
        UserModel = get_user_model()

        # Creates the new user.
        user = UserModel.objects.create_user(
            data['username'], email=data['email']
        )

        # Updates the user data.
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()

        return user

    def retrieve_user_data(self):
        """
        Retrieve the available user data from the service's API.
        """
        profile = self.get_profile()
        profiled_client = self.client_class(profile)

        return profiled_client.retrieve_user_data()

    def get_context_data(self, **kwargs):
        context = super(OAuthSetupView, self).get_context_data(**kwargs)
        context['service'] = self.client.service_name
        context['form'] = kwargs.get('form', settings.SETUP_FORM_CLASS(kwargs))

        return context

    def get(self, request, *args, **kwargs):
        # Protects the view to be accessed by non OAuth requests.
        if (request.user.is_authenticated() or
                not self.session_get('service_uid')):

            return HttpResponseForbidden()

        # Fetches the current OAuth profile.
        profile = self.get_profile()

        # If the profile has no user tries to attach the current user to it,
        # if the user is not logged in then creates a new one.
        if profile.user is None:
            # Fetches the user data from the service.
            UserModel = get_user_model()
            user_data = self.retrieve_user_data()
            check = lambda k: k in user_data and user_data[k]

            if settings.EMAIL_IS_USERNAME and check('email'):
                user_data.update(username=user_data['email'])

            # Check if the retrieved data is enough to create a new user or
            # fetch an existing user instance from the database.
            # If a existent user matches the data then links the OAuth profile
            # to its account.
            if check('email'):
                filters = {'email__iexact': user_data['email']}

                try:
                    user = UserModel.objects.get(**filters)
                    created = False

                except UserModel.DoesNotExist:
                    user = None
                    created = False

                if user is None and check('username'):
                    filters = {'username__iexact': user_data['username']}

                    if not UserModel.objects.filter(**filters):
                        user = self.create_new_user(user_data)
                        created = True

                if user is not None:
                    # Attaches the user to the profile.
                    profile.user = user
                    profile.save()

                    service = self.client.service_name.lower()

                    # Tells to the site that the user has linked its profile.
                    connect.send(sender=self.__class__, user=user,
                                 service=service)

                    # If the user was retrieved from the database and it is
                    # not active and ```ACTIVATE_ALREADY_REGISTERED_USERS```
                    # is True in settings then activates the user account and
                    # tell the site that the user was activated.
                    if (not created and not user.is_active and
                            settings.ACTIVATE_ALREADY_REGISTERED_USERS):

                        user.is_active = True
                        user.save()

                        activation.send(
                            sender=self.__class__, user=user,
                            service=service
                        )

                    # Authenticates the new user.
                    self.client.login(request, self.session_get('service_uid'))

                    # Tells to the site that the user was logged in.
                    login.send(sender=self.__class__, user=user,
                               service=service)

                    # Redirects the user to the proper url.
                    return redirect(self.get_redirect_url())

            # If no user was matched or created then redirect the user to the
            # final sertup view.
            # Suggest an username that does not exists in the site.
            user_data['username'] = compose_username(user_data)

            # Redirect the user to a custom setup url if provided.
            if self.setup_url is not None:
                url = reverse(self.setup_url)
                response = redirect(self._build_absolute_uri(url))

                # Set a temporal cookie with a max age of 2 minutes with the
                # user retrieved data to facilitate access for views that does
                # not depende on django rendering. The data is dumped as JSON
                # and then base64 endoced to can be correctly stored in the
                # cookie without braking it.
                encoded_data = b64encode(json.dumps(user_data))
                response.set_cookie('dsnstp', encoded_data, max_age=120)

                return response

            # Otherwise render the form to setup the user data.
            context = self.get_context_data(**user_data)

            return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # Protects the view to be accessed by non OAuth requests.
        if (request.user.is_authenticated() or
                not self.session_get('service_uid')):

            return HttpResponseForbidden()

        # Fetches the current OAuth profile.
        profile = self.get_profile()
        form = settings.SETUP_FORM_CLASS(request.POST)

        if form.is_valid():
            # Composes the data for the user creation.
            user_data = {
                'email': form.cleaned_data['email'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name']
            }

            # Sets the user's username.
            if settings.EMAIL_IS_USERNAME:
                user_data.update({'username': user_data['email']})
            else:
                user_data.update({'username': form.cleaned_data['username']})

            # Gets a new user and attaches it to the profile.
            user = self.create_new_user(user_data)
            profile.user = user
            profile.save()

            # Tells to the site that the user has connected its profile.
            connect.send(
                sender=self.__class__, user=user,
                service=self.client.service_name.lower()
            )

            # Authenticates the new user.
            self.client.login(request, self.session_get('service_uid'))

            # Tells to the site that the user was logged in.
            login.send(
                sender=self.__class__, user=user,
                service=self.client.service_name.lower()
            )

            # Redirects the user to the proper url.
            response = redirect(self.get_redirect_url())
            response.delete_cookie('dsnstp')

            return response

        else:
            if self.setup_url is not None:
                url = reverse(self.setup_url)
                response = redirect(self._build_absolute_uri(url))

                # Set a temporal cookie with a max age of 2 minutes with the
                # user retrieved data to facilitate access for views that does
                # not depende on django rendering. The data is dumped as JSON
                # and then base64 endoced to can be correctly stored in the
                # cookie without braking it.
                encoded_data = b64encode(json.dumps(form.data))
                response.set_cookie('dsnstp', encoded_data, max_age=120)

                return response

            # Otherwise render the form to setup the user data.
            context = self.get_context_data(**{'form': form})

            return self.render_to_response(context)

    def get_redirect_url(self):
        """
        Return the url to redirect the user when the setup of the new account
        has successfully finished.
        """
        url = self.session_pop('next') or '/'

        return self._build_absolute_uri(url)


class OAuthDisconnectView(OAuthMixin, View):
    """
    Base view that handles the flow to disconnect a service account from a
    site account.
    """
    def get_profile(self):
        # Tries to return the OAuth profile by retrieving the current
        # user's id.
        try:
            return self.client.model.objects.get(
                user__id=self.request.user.id)

        except self.client.model.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        # Fetches the OAuth profile.
        profile = self.get_profile()

        # If the profile is given then deletes it.
        if profile:
            user = profile.user
            profile.delete()

            # Tells to the site that the profile was disconnected.
            disconnect.send(
                sender=self.__class__, user=user,
                service=self.client.service_name.lower()
            )

            # Tells to the user that the disconnection was successful.
            tags = 'social %s' % self.client.service_name.lower()
            messages.success(request, _(
                'Your %(service)s profile was successfully disconnected from '
                'your user account.'
            ) % {'service': self.client.service_name}, extra_tags=tags)

        return redirect(request.POST.get('next', '/'))
