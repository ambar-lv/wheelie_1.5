from django.db import models
from apps.core.abstraction import AbstractBaseModel
from django.utils.translation import gettext_lazy as _
from apps.user.models import User


class TelegramBotRelation(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='telegram_bot_confirmations', verbose_name=_('User'))
    message_id = models.IntegerField(_('Message ID'))
    button_id = models.IntegerField(_('Button ID'))

    class Meta:
        verbose_name = _("Telegram bot relation")
        verbose_name_plural = _("Telegram bot relations")


class OCRLicense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ocr_licenses', verbose_name=_('User'))
    pk_ocr = models.CharField(_('OCR pk'), max_length=255, blank=True, null=True)
    name_ocr = models.CharField(_('OCR name'), max_length=255, blank=True, null=True)
    family_ocr = models.CharField(_('OCR family'), max_length=255, blank=True, null=True)
    birth_ocr = models.CharField(_('OCR birth'), max_length=255, blank=True, null=True)
    reg_ocr = models.CharField(_('OCR reg'), max_length=255, blank=True, null=True)
    org_ocr = models.CharField(_('OCR organisation'), max_length=255, blank=True, null=True)
    expire_ocr = models.CharField(_('OCR expire'), max_length=255, blank=True, null=True)
    nr_ocr = models.CharField(_('OCR number'), max_length=255, blank=True, null=True)
    source_ocr = models.TextField(_('OCR source text'), blank=True, null=True)
    is_active = models.BooleanField(_('Active'), default=True)

    def __str__(self):
        return self.name_ocr

    class Meta:
        verbose_name = _("OCR license")
        verbose_name_plural = _("OCR licenses")
