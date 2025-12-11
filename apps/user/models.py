from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from apps.user.enums import LanguageChoice, LegalChoice
from apps.core.abstraction import AbstractBaseModel, AbstractGeoModel
from apps.core.models import Country, City
from apps.trip.models import Trip
from apps.trailer.models import Trailer
from apps.company.models import Company
from apps.employer.models import Employer


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Each user has to have a phone number")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser, AbstractBaseModel, AbstractGeoModel):
    # TODO: Не добавлена связь с бонусами
    username = None
    device = models.CharField(_('Device'), null=True, blank=True, max_length=10)
    balance = models.DecimalField(_('Balance'), max_digits=12, decimal_places=2, default=0.00)
    lang = models.CharField(_('Language'), max_length=50, choices=LanguageChoice.choices, default=LanguageChoice.RU)
    phone_code = models.PositiveSmallIntegerField(_("Phone code"))
    phone = models.PositiveIntegerField(_('Phone'), unique=True)
    email = models.EmailField(_('Email'), null=True, blank=True)
    email_code = models.PositiveSmallIntegerField(_('Email code'), null=True, blank=True)
    first_name = models.CharField(_('First name'), null=True, blank=True, max_length=255)
    last_name = models.CharField(_('Last name'), null=True, blank=True, max_length=255)
    token = models.CharField(_('Token'), max_length=255, null=True, blank=True)
    code = models.PositiveSmallIntegerField(_('Code'), null=True, blank=True)

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Country'), related_name='users')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('City'), related_name='users')
    address = models.TextField(_('Address'), null=True, blank=True)
    zip_code = models.CharField(_('Zip code'), max_length=10, null=True, blank=True)

    reg_ip = models.GenericIPAddressField(_("Registration IP"), null=True, blank=True)
    last_ip = models.GenericIPAddressField(_("Last IP"), null=True, blank=True)
    
    legal = models.CharField(_("Legal"), choices=LegalChoice.choices, null=True, blank=True, max_length=3)
    comments = models.TextField(_("Сomments"), null=True, blank=True)

    employer = models.ForeignKey(Employer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Employer'))

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"+{self.phone_code}{self.phone}"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class UserTrip(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name=_("Trip"))
    trailer = models.ForeignKey(Trailer, on_delete=models.CASCADE, verbose_name=_("Trailer"))
    booked_at = models.DateTimeField(_('Booked at'))
    started_at = models.DateTimeField(_('Started at'), null=True, blank=True)

    def __str__(self):
        return f"{self.user.phone}: {self.trip.id}"

    class Meta:
        verbose_name = _("User trip")
        verbose_name_plural = _("User trips")


class UserDocument(AbstractBaseModel):
    def license_front_upload(instance, filename):
        return f'user/{instance.user.id}/license-front/{filename}'

    def license_back_upload(instance, filename):
        return f'user/{instance.user.id}/license-back/{filename}'

    def selfie_upload(instance, filename):
        return f'user/{instance.user.id}/selfie/{filename}'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    driver_license = models.ImageField(_('Driver license'), upload_to=license_front_upload, null=True, blank=True)
    driver_license_back = models.ImageField(_('Driver license back'), upload_to=license_back_upload, null=True, blank=True)
    driver_license_expire = models.DateField(_('Driver license expire'), null=True, blank=True)
    selfie = models.ImageField(_('Selfie'), upload_to=selfie_upload, null=True, blank=True)

    class Meta:
        verbose_name = _("User document")
        verbose_name_plural = _("User documents")
