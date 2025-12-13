from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.abstraction import AbstractBaseModel
from apps.core.enums import ActivityStatusChoice
from apps.workforce.models import Owner


class Country(models.Model):
    name = models.CharField(_('Name'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ['name']


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_("Country"))
    name = models.CharField(_('Name'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        ordering = ['name']


class Invoice(AbstractBaseModel):
    logo = models.ImageField(_('Logo'), upload_to='invoice_logos/', null=True, blank=True)
    logo_height_pt = models.PositiveSmallIntegerField(_('Logo height in pt'), default=95)
    address = models.CharField(_('Address'), max_length=255)
    name = models.CharField(_('Name'), max_length=255)
    fax = models.CharField(_('Fax'), max_length=100, blank=True, null=True)
    reg = models.CharField(_('Registration number'), max_length=50)
    pvn = models.CharField(_('PVN'), max_length=50)
    bank = models.CharField(_('Bank'), max_length=255)
    swift = models.CharField(_('SWIFT'), max_length=100)
    ibis = models.CharField(_('Ibis'), max_length=255, blank=True, null=True)
    warning = models.CharField(_('Warning'), max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')


class Project(AbstractBaseModel):
    #tpl desing(what is tpl? template? where can i find it?)
    name = models.CharField(_('Name'), max_length=255, unique=True)
    domain = models.CharField(_('Domain'), max_length=255, null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name=_("Owner"))
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Invoice"))
    recaptcha = models.BooleanField(_("reCAPTCHA"), default=False)
    status = models.CharField(_("Activity status"), choices=ActivityStatusChoice.choices, default=ActivityStatusChoice.YES, max_length=3)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class ProjectVersion(AbstractBaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_('Project'))
    apple_version = models.CharField(_('Apple Version'), max_length=20)
    android_version = models.CharField(_('Android Version'), max_length=20)
    apple_update_link = models.URLField(_('Apple update link'))
    android_update_link = models.URLField(_('Android update link'))
    test_phones = models.TextField(_('Test phones'), null=True, blank=True, help_text=_('estnumbers, without +371, separate with "," or ";" or "NEWLINE"'))

    def __str__(self) -> str:
        return f"{self.project} - iOS:{self.apple_version}, Android:{self.android_version};"

    class Meta:
        verbose_name = _("Version")
        verbose_name_plural = _("Versions")


class ProjectImage(AbstractBaseModel):
    def image_upload(instance, filename):
        return f'project/{instance.project.id}/{filename}'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_('Project'))
    main = models.ImageField(_('Main image'), upload_to=image_upload)
    slider = models.ImageField(_('Slider image'), upload_to=image_upload)

    class Meta:
        verbose_name = _("Project image")
        verbose_name_plural = _("Project images")


class ReferalPercent(AbstractBaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_('Project'))
    new = models.PositiveSmallIntegerField(_('Percent for newcomers'), default=0)
    sharing = models.PositiveSmallIntegerField(_('Percent for sharing'), default=0)
    
    class Meta:
        verbose_name = _("Project referal percent")
        verbose_name_plural = _("Project referal procents")
