from datetime import timedelta
from urlparse import urlparse, parse_qs

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View, TemplateView

from socialnetworks.base.settings import (
    EMAIL_IS_USERNAME, SETUP_FORM_CLASS, SETUP_TEMPLATE
)
from socialnetworks.signals import connect, disconnect, login


class OAuthMixin(object):
    """
    Mixin that defines the necessary methods for OAuth views.
    OAuth views must be inherited from this class.

    """
    # The client that defines the necessary information to perform
    # the OAuth flow.
    client = None

    def __get_session(self):
        """
        Returns the current session's object to store the data that will
        be used trough the OAuth flow.

        """
        if self.client.session_key not in self.request.session:
            self.request.session[self.client.session_key] = {}

        return self.request.session[self.client.session_key]

    def __set_session(self, dictionary):
        """
        Updates the current session's object, useful if the backend is not
        configured to save session in every request.

        """
        self.request.session[self.client.session_key] = dictionary

    def session_get(self, key):
        """
        Returns the provided key value from the current session's object. If
        key is not in the object returns None.

        """
        return self.__get_session().get(key, None)

    def session_put(self, **dictionary):
        """
        Puts the given dictionary into the current session's object.

        """
        session = self.__get_session()
        session.update(**dictionary)
        self.__set_session(session)

    def session_pop(self, key):
        """
        Returns the provided key value from the current session's object and
        removes the key from the object. If key is not in the object returns
        None.

        """
        session = self.__get_session()
        value = session.pop(key, None)
        self.__set_session(session)

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
        Returns the url where the user will be redirected after when the
        access token is requested.

        """
        raise NotImplementedError

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


class OAuthDialogRedirectView(View, OAuthMixin):
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

            # Appends the response to the user session.
            self.session_put(**{
                'request_token': credentials.get('oauth_token'),
                'request_token_secret': credentials.get('oauth_token_secret')
            })

        # Redirects the user to the authorization dialog.
        return redirect(self.get_redirect_url())


class OAuthCallbackView(View, OAuthMixin):
    """
    Base view that handles the callback redirection from the service.

    """
    def get(self, request, *args, **kwargs):
        # Protects the view to be accessed by non OAuth requests.
        if self.client.verifier_label not in request.GET:
            return HttpResponseForbidden()

        # Gets the OAuth access token.
        if self.client.oauth_version == 1:
            credentials = self.client.get_access_token(
                request_token=self.session_get('request_token'),
                request_token_secret=self.session_get('request_token_secret'),
                verifier=request.GET[self.client.verifier_label]
            )
        elif self.client.oauth_version == 2:
            credentials = self.client.get_access_token(
                verifier=request.GET[self.client.verifier_label],
                callback=self.get_callback_url(),
            )

        # Verifies if the service's user id was provided in the credentials,
        # if it is not provided the fetches is by debugging the access token.
        access_token = credentials.get(self.client.access_token_label, None)
        service_uid = credentials.get(self.client.uid_label, None)
        token_expiration = credentials.get(self.client.expiration_label, None)

        # Calculates the token expiration date.
        if token_expiration:
            token_expiration = (
                timezone.now() + timedelta(seconds=int(token_expiration)))

        # Debugs the token.
        if not service_uid:
            token_is_valid, debugged_data = self.client.debug_access_token(
                access_token)
            if token_is_valid:
                service_uid = debugged_data.get(self.client.uid_label)

        # Appends the response to the user session.
        self.session_put(**{
            'access_token': credentials.get(
                self.client.access_token_label),
            'access_token_secret': credentials.get(
                self.client.access_token_secret_label),
            'service_uid': service_uid
        })

        # Gets the lookups to retrieve or create the profile.
        lookup_kwargs = {
            'service_uid': self.session_get('service_uid')
        }

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

        # Updates the profile to make sure that we have always the most
        # recent token.
        profile.oauth_access_token = self.session_get('access_token')

        if self.client.oauth_version == 1:
            profile.oauth_request_token = self.session_get('request_token')
            profile.oauth_request_token_secret = self.session_get(
                'request_token_secret')
            profile.oauth_access_token_secret = self.session_get(
                'access_token_secret')

        if self.client.oauth_version == 2:
            profile.oauth_access_token_expires_at = (
                token_expiration if token_expiration else None)

        profile.save()

        # If the profile was created or has no user, tries to attach the
        # profile to current user, if the user is not logged in redirects
        # it to the final setup view to create a new one.
        if created or not profile.user:
            if request.user.is_authenticated():
                profile.user = self.request.user
                profile.save()

                # Tells to the site that the user has connected its profile.
                connect.send(
                    sender=self, user=self.request.user,
                    service=self.client.service_name.lower()
                )

                # Tells to the user that his connection was successful.
                messages.success(request, _(
                    'Your %(service)s profile was successfully connected '
                    'with your user account.'
                ) % {'service': self.client.service_name})

            else:
                self.session_put(**{'new_user': True})

        elif (profile.user and profile.user != self.request.user and
                self.request.user.is_authenticated()):

            # Tells to the user that his connection was unsuccessful.
            messages.error(request, _(
                'This %(service)s profile is already connected with another '
                'user account.'
            ) % {'service': self.client.service_name})

        else:
            # Logs the user in if it is not logged yet.
            self.client.login(request, self.session_get('service_uid'))

            # Tells to the site that the user was logged in.
            login.send(
                sender=self, user=self.request.user,
                service=self.client.service_name.lower()
            )

        return redirect(self.get_redirect_url())


class OAuthSetupView(TemplateView, OAuthMixin):
    """
    Base View that handles the setup for the account after the access
    token is provided.

    """
    template_name = SETUP_TEMPLATE

    def get_profile(self):
        # Tries to return the OAuth profile by retrieving the service_uid
        # in the current session.
        try:
            return self.client.model.objects.get(
                service_uid=self.session_get('service_uid'))

        except self.client.model.DoesNotExist:
            return None

    def create_new_user(self, data):
        # Creates the new user.
        user = User.objects.create_user(
            data['username'], email=data['email']
        )

        # Updates the user data.
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()

        return user

    def get_context_data(self, **kwargs):
        context = super(OAuthSetupView, self).get_context_data(**kwargs)
        context['service'] = self.client.service_name
        context['form'] = kwargs.get('form', SETUP_FORM_CLASS(kwargs))
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
        if not profile.user:
            # Fetches the user data from the service.
            user_data = self.retrieve_user_data()

            if EMAIL_IS_USERNAME and 'email' in user_data:
                user_data.update({'username': user_data['email']})

            # If the data is incomplete then redirects the user to the final
            # setup form.
            if ('username' not in user_data or 'email' not in user_data or
                    [(k, v) for k, v in user_data.items() if k in
                        ['username', 'email'] and not v]):

                return self.render_to_response(
                    self.get_context_data(**user_data))

            else:
                # Tries to fetch an exiting user with that matches the data
                # retrieved from the service.
                try:
                    username_filter = Q(username=user_data['username'])
                    email_filter = Q(email=user_data['email'])
                    user = User.objects.get(username_filter | email_filter)

                # If no user is found, then creates a new user with the data
                # retrieved from the service.
                except User.DoesNotExist:
                    user = self.create_new_user(user_data)

                # Attaches the user to the profile.
                profile.user = user
                profile.save()

                # Tells to the site that the user has connected its profile.
                connect.send(
                    sender=self, user=user,
                    service=self.client.service_name.lower()
                )

                # Authenticates the new user.
                self.client.login(request, self.session_get('service_uid'))

                # Tells to the site that the user was logged in.
                login.send(
                    sender=self, user=user,
                    service=self.client.service_name.lower()
                )

                # Redirects the user to the proper url.
                return redirect(self.get_redirect_url())

    def post(self, request, *args, **kwargs):
        # Protects the view to be accessed by non OAuth requests.
        if (request.user.is_authenticated() or
                not self.session_get('service_uid')):

            return HttpResponseForbidden()

        # Fetches the current OAuth profile.
        profile = self.get_profile()

        form = SETUP_FORM_CLASS(request.POST)
        if form.is_valid():
            # Composes the data for the user creation.
            user_data = {
                'email': form.cleaned_data['email'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name']
            }

            # Sets the user's username.
            if EMAIL_IS_USERNAME:
                user_data.update({'username': user_data['email']})
            else:
                user_data.update({'username': form.cleaned_data['username']})

            # Gets a new user and attaches it to the profile.
            user = self.create_new_user(user_data)
            profile.user = user
            profile.save()

            # Tells to the site that the user has connected its profile.
            connect.send(
                sender=self, user=user,
                service=self.client.service_name.lower()
            )

            # Authenticates the new user.
            self.client.login(request, self.session_get('service_uid'))

            # Tells to the site that the user was logged in.
            login.send(
                sender=self, user=user,
                service=self.client.service_name.lower()
            )

            # Redirects the user to the proper url.
            return redirect(self.get_redirect_url())

        else:
            return self.render_to_response(self.get_context_data(
                **{'form': form}))


class OAuthDisconnectView(View, OAuthMixin):
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
                sender=self, user=user,
                service=self.client.service_name.lower()
            )

            # Tells to the user that the disconnection was successful.
            messages.success(request, _(
                'Your %(service)s profile was successfully disconnected from '
                'your user account.'
            ) % {'service': self.client.service_name})

        return redirect(request.POST.get('next', '/'))
