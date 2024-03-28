from django.contrib import admin

from solo.admin import SingletonModelAdmin

from django_license_wall.models import LicenseKey
from django_license_wall.forms import LicenseForm


admin.site.login_form = LicenseForm
admin.site.login_template = 'django_license_wall/login.html'


class LicenseKeyAdmin(SingletonModelAdmin):
    pass


admin.site.register(LicenseKey, LicenseKeyAdmin)
