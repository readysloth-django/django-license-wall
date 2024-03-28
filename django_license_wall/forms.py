from django import forms

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class LicenseForm(forms.Form):
    license = forms.CharField()

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def clean(self):
        self.user = authenticate(
            self.request,
            license=self.cleaned_data['license']
        )
        if not self.user:
            raise ValidationError(
                'You should supply valid license to use application',
                code='invalid_login',
                params={'license': 'invalid_license'}
            )
        self.user_cache = self.user
        return self.cleaned_data

    def get_user(self):
        return self.user_cache
