from django.contrib.auth import forms as auth_form
from django.core.exceptions import ValidationError

class AuthenticationForm(auth_form.AuthenticationForm):

    def confirm_login_allowed(self, user):
        super(AuthenticationForm, self).confirm_login_allowed(user)

        if not user.is_active:
            raise ValidationError("user is not active")
