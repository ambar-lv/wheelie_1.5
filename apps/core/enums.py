from django.db import models
from django.utils.translation import gettext_lazy as _


class ActivityStatusChoice(models.TextChoices):
    YES = 'yes', _('Yes')
    NO = 'no', _('No')
    DEL = 'del', _('Del')
