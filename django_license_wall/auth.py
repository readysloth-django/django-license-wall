from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from django_license_wall.license import LicenseKey
from django_license_wall.models import LicenseKey as LicenseKeyModel


USER_MODEL = get_user_model()


class LicenseBackend(ModelBackend):
    def authenticate(self, request, license=None):
        username = 'owner'
        existing_license = None
        try:
            existing_license = LicenseKeyModel.objects.get()
        except LicenseKeyModel.DoesNotExist:
            pass

        new_license_valid = LicenseKey.verify(license)
        existing_license_valid = False
        if existing_license:
            existing_license_valid = LicenseKey.verify(existing_license.key)

        if new_license_valid:
            if existing_license:
                existing_license.delete()
            LicenseKeyModel.objects.create(key=license)
        if new_license_valid or existing_license_valid:
            user, _ = USER_MODEL.objects.get_or_create(
                username=username,
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            return user
