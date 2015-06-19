from django import forms
from django.contrib.auth.models import User
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from .settings import EMAIL_IS_USERNAME


class SocialUserCreationForm(forms.ModelForm):
    """
    Form that handles the validation of the social users setup.
    """
    username = forms.RegexField(
        required=not EMAIL_IS_USERNAME,
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        error_messages={'invalid': _('This value may contain only letters, '
                        'numbers and @/./+/-/_ characters.')},
        label=capfirst(_('username'))
    )

    email = forms.EmailField(
        required=EMAIL_IS_USERNAME,
        max_length=75,
        label=capfirst(_('email'))
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(SocialUserCreationForm, self).__init__(*args, **kwargs)

        # If the email is used as username in the site, then do not show
        # this field on the form.
        if EMAIL_IS_USERNAME:
            del self.fields['username']

    def clean_username(self):
        """
        Verifies that the given username is not used by any already
        registered user in the site.
        """
        try:
            user = User.objects.get(username=self.cleaned_data['username'])

        except User.DoesNotExist:
            user = None

        if user is not None:
            raise forms.ValidationError(_(
                'This username is already in use, please provide a '
                'different username.'
            ))

        return self.cleaned_data['username']

    def clean_email(self):
        """
        Verifies that the given email address is not used by any already
        registered user in the site.
        """
        try:
            user = User.objects.get(email=self.cleaned_data['email'])

        except User.DoesNotExist:
            user = None

        if user is not None:
            raise forms.ValidationError(_(
                'This email address is already in use, please provide a '
                'different email address.'
            ))

        return self.cleaned_data['email']
