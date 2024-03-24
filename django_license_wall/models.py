from django.db import models
from django.utils.translation import gettext_lazy as _

from solo.models import SingletonModel


class LicenseKey(SingletonModel):
    key = models.CharField(_('Key'), max_length=32)

    class Meta:
        verbose_name = _('License key')
        verbose_name_plural = _('License keys')

    def __str__(self):
        return self.key
