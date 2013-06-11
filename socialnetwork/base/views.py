from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic.base import View

from socialnetwork.signals import connect, disconnect, login


class BaseOAuthView(View):
    """
    Base class for the OAuth flow.
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
        if self.client.session_key not in self.__request.session:
            self.__request.session[self.client.session_key] = {}

        return self.__request.session[self.client.session_key]

    def __set_session(self, dictionary):
        """
        Updates the current session's object, useful if the backend is not
        configured to save session in every request.

        """
        self.__request.session[self.client.session_key] = dictionary

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
        if self.client.session_key in self.__request.session:
            del self.__request.session[self.client.session_key]

    def get_redirect_url(self):
        """"
        Returns the url where the user will be redirected after its request
        is processed.

        Subclasses must implement this method.

        """
        raise NotImplementedError

    def dispatch(self, request, *args, **kwargs):
        """
        Sets the current request as an atrribute, this way it can be accessed
        easily by the methods that modifies the user session.

        """
        self.__request = request
        return super(BaseOAuthView, self).dispatch(request, *args, **kwargs)


class OAuthDialogRedirectView(BaseOAuthView):
    """
    Base view that handles the service's auth/login dialog request.

    """
    def get(self, request):
        # Clears the current user's session to avoid the use of old
        # login information.
        self.session_clear()

        # Fetches the url where the user will be redirected when the
        # flow ends and stores it in the user's session.
        if 'next' in request.GET:
            self.session_put(**{
                'next': request.GET['next']
            })

        else:
            self.session_put(**{
                'next': '/'
            })

        # Makes the request of the login/auth dialog to the service.
        return redirect(self.get_redirect_url())


class OAuthCallbackView(BaseOAuthView):
    """
    Base view that handles the callback redirection from the service.

    """
    def get(self, request):
        # Protect the view to be accessed by non OAuth requests.
        if 'code' not in request.GET:
            return HttpResponseForbidden()

        # Request the access token to the service
        token = self.client.request_access_token(request.GET['code'])

        # If the given access token is valid then tries to login or create
        # the user, if the token is invalid then redirects to the start of
        # the flow.
        token_is_valid, token_debug = self.client.debug_access_token(token)

        if token_is_valid:
            self.session_put(**{
                'access_token': token,
                'expires_at': token_debug['expires_at'],
                'uid': token_debug['user_id'],
            })

            # Gets or creates the profile in the service
            profile, created = self.client.model.objects.get_or_create(
                service_uid=self.session_get('uid')
            )

            # If the given access_token does not match the token stored in
            # the db updates the profile with the new access token.
            if profile.oauth_access_token != token:
                profile.oauth_access_token = token
                profile.oauth_access_token_expires_at = (
                    datetime.fromtimestamp(self.session_get('expires_at'))
                )
                profile.save()

            # If the profile was created or has no user, tries to attach the
            # the profile to current user, if the user is not logged in
            # redirects it to the final setup view to create a new one.
            if created or not profile.user:
                if request.user.is_authenticated():
                    profile.user = self.request.user
                    profile.save()
                    connect.send(
                        sender=self, user=self.request.user,
                        service=self.client.service_name.lower()
                    )
                    messages.success(self.request, _('Your %(service)s '
                        'profile was successfully connected with your '
                        'user account.' % {
                            'service': self.client.service_name
                        })
                    )
                else:
                    self.session_put(**{'new_user': True})

            elif (profile.user and profile.user != self.request.user and
                  self.request.user.is_authenticated()):
                    messages.error(self.request, _('This %(service)s profile '
                        'is already connected with another user account.' % {
                            'service': self.client.service_name
                        })
                    )
                    return redirect(self.get_redirect_url())

            else:
                # Logs the user in if it is not logged yet.
                self.client.login(request, self.session_get('uid'))
                login.send(
                    sender=self, user=self.request.user,
                    service=self.client.service_name.lower()
                )

            return redirect(self.get_redirect_url())


class OAuthSetupView(BaseOAuthView):
    """
    Base View that handles the setup for the account after the access
    token is provided.

    """
    def retrieve_user_data(self):
        """
        Returns a dictionary with the keys 'first_name', 'last_name', 'email'
        and 'username'. The values for the keys should be retrieved from the
        service.

        Subclasses must implement this method.

        """
        raise NotImplementedError

    def get(self, request):
        # Protect the view to be accessed by non logged users.
        if request.user.is_authenticated():
            return HttpResponseForbidden()

        # Fetches the profile that corresponds to the service uid.
        profile = self.client.model.objects.get(service_uid=self.session_get('uid'))

        # If the profile has no user tries to fetch an already registered
        # user with the retrieved username/email. If the looked user does
        # not exist creates a new one with all the retrieved data.
        if not profile.user:
            data = self.retrieve_user_data()

            try:
                user = User.objects.get(
                    username=data['username'], email=data['email']
                )
            except User.DoesNotExist:
                # Gets the extra data to create the new user.
                extra_fields = dict(filter(
                    lambda i: i[0] in ['first_name', 'last_name'],
                    data.items()
                ))

                # Creates the new user.
                user = User.objects.create_user(
                    data['username'], email=data['email'], **extra_fields
                )

            profile.user = user
            profile.save()
            connect.send(
                sender=self, user=user,
                service=self.client.service_name.lower()
            )

        # Authenticates the new user.
        self.client.login(request, self.session_get('uid'))
        login.send(
            sender=self, user=user,
            service=self.client.service_name.lower()
        )

        # Redirects the user to the proper url.
        return redirect(self.get_redirect_url())


class BaseProfileDisconnectView(View):
    """
    Base view that handles social profiles disconnection.

    """
    client = None

    def get_profile(self):
        """
        Returns the current profile object that will be deleted.
        Subclasses must implement this method.

        """
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        profile = self.get_profile()
        if profile:
            user = profile.user
            profile.delete()
            disconnect.send(
                sender=self, user=user,
                service=self.client.service_name.lower()
            )

        messages.success(self.request, _('Your %(service)s profile was '
            'successfully disconnected from your user account.' % {
                'service': self.client.service_name
            })
        )

        if 'next' in request.POST:
            return redirect(request.POST['next'])
        else:
            return redirect('/')
