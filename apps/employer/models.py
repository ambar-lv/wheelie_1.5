from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.abstraction import AbstractBaseModel


class Employer(AbstractBaseModel):
    name = models.CharField(_('Name'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Employer")
        verbose_name_plural = _("Employers")
        ordering = ['name']
