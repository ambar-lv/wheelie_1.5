from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.abstraction import AbstractBaseModel, AbstractGeoModel
from apps.core.enums import ActivityStatusChoice
from parler.models import TranslatableModel, TranslatedFields
from django.core.validators import FileExtensionValidator, validate_image_file_extension


class TrailerCategory(TranslatableModel, AbstractBaseModel):
    code = models.CharField(_('Code'), max_length=255)
    icon = models.ImageField(
        _("Icon"),
        help_text=_('Format: PNG, size: 512*512 px'),
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['png']),
            validate_image_file_extension,
        ]
    )
    project = models.ForeignKey('core.Project', on_delete=models.CASCADE, verbose_name=_('Project'))
    translations = TranslatedFields(
        title=models.CharField('Title', max_length=255),
        description=models.TextField('Description')
    )
    status = models.CharField(_("Activity status"), choices=ActivityStatusChoice.choices, default=ActivityStatusChoice.YES, max_length=3)

    def __str__(self) -> str:
        return self.code

    class Meta:
        verbose_name = _('Trailer category')
        verbose_name_plural = _('Trailer categories')


class TrailerType(TranslatableModel, AbstractBaseModel):
    def trailer_type_image(instance, filename):
        return f'trailer-types/{instance.id}/{filename}'

    translations = TranslatedFields(
        topic=models.CharField('Topic', max_length=255),
        title=models.CharField('Title', max_length=255),
        text=models.TextField('Text'),
        subtext=models.TextField('Sub text')
    )
    code = models.CharField(_("Code"), max_length=50)
    minimum_license = models.CharField(_("Minimum licence"), max_length=5)
    brutto = models.PositiveSmallIntegerField(_("Brutto"), default=0)
    netto = models.PositiveSmallIntegerField(_("Netto"), default=0)
    pins = models.PositiveSmallIntegerField(_("Pins"), default=7)
    sizes = models.CharField(_("Sizes"), max_length=50)
    category = models.ForeignKey(TrailerCategory, on_delete=models.CASCADE, verbose_name=_("Category"))
    main_image = models.ImageField(
        _('Image'),
        upload_to=trailer_type_image,
        help_text=_("Format: .PNG, size: 1980 * 1280 px"),
        validators=[
            FileExtensionValidator(allowed_extensions=['png']),
            validate_image_file_extension,
        ]
    )
    icon = models.ImageField(
        _('Icon'),
        upload_to=trailer_type_image,
        help_text=_("Format: .PNG, size: 512 * 512 px"),
        validators=[
            FileExtensionValidator(allowed_extensions=['png']),
            validate_image_file_extension,
        ]
    )
    position = models.PositiveSmallIntegerField(_("Position"), default=0)
    status = models.CharField(_("Activity status"), choices=ActivityStatusChoice.choices, default=ActivityStatusChoice.YES, max_length=3)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = _('Trailer type')
        verbose_name_plural = _('Trailer types')


class TrailerTypeSEO(TranslatableModel, AbstractBaseModel):
    trailer_type = models.ForeignKey(TrailerType, on_delete=models.CASCADE, verbose_name=_('Trailer type'), related_name='seo')
    translations = TranslatedFields(
        title=models.CharField('Title', max_length=255, null=True, blank=True),
        description=models.TextField('Description', null=True, blank=True),
        keywords=models.TextField('Keywords', null=True, blank=True),
        url = models.SlugField(_("URL"), null=True, blank=True),
        img = models.ImageField(
            _("Image"),
            help_text=_('Format: PNG, size: 512*512 px'),
            null=True,
            blank=True,
            validators=[
                FileExtensionValidator(allowed_extensions=['png']),
                validate_image_file_extension,
            ]
        ),
        link = models.CharField(_("Link"), max_length=255)
    )

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        verbose_name = _('Trailer type SEO')
        verbose_name_plural = _('Trailer type SEO')


class TrailerTypePrice(AbstractBaseModel):
    trailer_type = models.ForeignKey(TrailerType, on_delete=models.CASCADE, verbose_name=_('Trailer type'), related_name='prices')
    hour = models.DecimalField(_("For hour"), max_digits=12, decimal_places=2)
    one_day = models.DecimalField(_("For one day"), max_digits=12, decimal_places=2)
    two_days = models.DecimalField(_("For two days"), max_digits=12, decimal_places=2)
    three_days = models.DecimalField(_("For three days"), max_digits=12, decimal_places=2)
    week = models.DecimalField(_("For week"), max_digits=12, decimal_places=2)
    month = models.DecimalField(_("For month"), max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        verbose_name = _('Trailer type price')
        verbose_name_plural = _('Trailer type prices')


class TrailerTypeImage(AbstractBaseModel):
    def trailer_type_image(instance, filename):
        return f'trailer-types/{instance.trailer_type.id}/{filename}'

    trailer_type = models.ForeignKey(TrailerType, on_delete=models.CASCADE, verbose_name=_('Trailer type'), related_name='images')
    number = models.PositiveSmallIntegerField(_('Number'))
    image = models.ImageField(
        _('Image'),
        upload_to=trailer_type_image,
        help_text=_("Format: .PNG, size: 1980 * 1280 px"),
        validators=[
            FileExtensionValidator(allowed_extensions=['png']),
            validate_image_file_extension,
        ]
    )

    def __str__(self) -> str:
        return str(self.number)

    class Meta:
        verbose_name = _('Trailer type image')
        verbose_name_plural = _('Trailer type images')
        unique_together = ['trailer_type', 'number']


class Parking(AbstractBaseModel, AbstractGeoModel):
    def parking_image(instance, filename):
        return f'parkings/{instance.trailer_type.id}/{filename}'
    #FINISHED HERE(TODO: parking owners=partner)
    project = models.ForeignKey('core.Project', on_delete=models.CASCADE, verbose_name=_('Project'))
    # partner?
    # guard ...
    name = models.CharField(_("Name"), max_length=255)
    address = models.CharField(_("Address"), max_length=255)
    working_hours = models.CharField(_("Working hours"), max_length=255)
    # Traccar Parking id relation?
    image = models.ImageField(_('Image'), upload_to=parking_image)
    parking_path = models.JSONField(_("Parking paths"), null=True, blank=True)


    def __str__(self) -> str:
        return self.id
    
    class Meta:
        verbose_name = _('Parking')
        verbose_name_plural = _('Parkings')


class Trailer(AbstractBaseModel, AbstractGeoModel):
    def trailer_passport(instance, filename):
        return f'trailers/{instance.id}/passports/{filename}'

    project = models.ForeignKey('core.Project', on_delete=models.CASCADE, verbose_name=_('Project'), related_name='trailers')
    owner = models.ForeignKey('workforce.Owner', on_delete=models.CASCADE, verbose_name=_('Owner'), related_name='owned_trailers')
    type = models.ForeignKey(TrailerType, on_delete=models.CASCADE, verbose_name=_('Type'), related_name='typed_trailers')
    # parking relation
    # ordered user relation
    number = models.CharField(_('State number'), max_length=50, unique=True)
    personal_price = models.DecimalField(_("Personal price"), max_digits=12, decimal_places=2, null=True, blank=True)
    personal_discount = models.DecimalField(_("Personal discount"), max_digits=12, decimal_places=2, null=True, blank=True)
    passport = models.ImageField(_("Technical passport"), null=True, blank=True, upload_to=trailer_passport, help_text=_('Format: .JPG, minimal width: 1280px'))
    status = models.CharField(_("Activity status"), choices=ActivityStatusChoice.choices, default=ActivityStatusChoice.YES, max_length=3)

    def __str__(self) -> str:
        return self.number

    class Meta:
        verbose_name = _('Trailer')
        verbose_name_plural = _('Trailers')


class TrailerSEO(TranslatableModel, AbstractBaseModel):
    trailer = models.ForeignKey(Trailer, on_delete=models.CASCADE, verbose_name=_('Trailer'), related_name='seo')
    translations = TranslatedFields(
        title=models.CharField('Title', max_length=255, null=True, blank=True),
        description=models.TextField('Description', null=True, blank=True),
        keywords=models.TextField('Keywords', null=True, blank=True),
        url = models.SlugField(_("URL"), null=True, blank=True),
        img = models.ImageField(
            _("Image"),
            help_text=_('Format: PNG, size: 512*512 px'),
            null=True,
            blank=True,
            validators=[
                FileExtensionValidator(allowed_extensions=['png']),
                validate_image_file_extension,
            ]
        ),
        link = models.CharField(_("Link"), max_length=255)
    )

    def __str__(self) -> str:
        return self.trailer.number

    class Meta:
        verbose_name = _('Trailer SEO')
        verbose_name_plural = _('Trailers SEO')
