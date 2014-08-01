from django.contrib.auth.backends import ModelBackend


class BaseSocialBackend(ModelBackend):
    """
    Base backend that handles the login with the social networks.
    """
    supports_object_permissions = False
    supports_anonymous_user = False

    # The model to lookup for the user
    model = None

    def authenticate(self, service_uid):
        try:
            profile = self.model.objects.get(
                service_uid=service_uid)

            return profile.user

        except self.model.DoesNotExist:
            return None
