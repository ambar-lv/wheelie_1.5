from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.abstraction import AbstractBaseModel
from apps.core.enums import ActivityStatusChoice
from apps.user.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
    
    
class Company(AbstractBaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Owner"))
    name = models.CharField(_('Name'), max_length=255)
    full_name = models.CharField(_('Full name'), max_length=255, null=True, blank=True)
    reg_number = models.CharField(_("Registration number"), max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

    @classmethod
    def get_by_natural_key(cls, name):
        return cls.objects.get(name=name)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ['name']


class Employer(AbstractBaseModel):
    name = models.CharField(_('Name'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Employer")
        verbose_name_plural = _("Employers")
        ordering = ['name']


class Owner(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    percent = models.SmallIntegerField(_("Percent"), default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    status = models.CharField(_("Activity status"), choices=ActivityStatusChoice.choices, default=ActivityStatusChoice.YES, max_length=3)

    def __str__(self) -> str:
        return str(self.user)

    def natural_key(self):
        return (self.user.phone,)

    @classmethod
    def get_by_natural_key(cls, phone):
        return cls.objects.get(user__phone=phone)

    class Meta:
        verbose_name = _("Owner")
        verbose_name_plural = _("Owners")

