from django.db import models
from django.utils.translation import gettext_lazy as _


class TrailerTypeChoice(models.TextChoices):
    SIGHT = 'sight', _('Sight')
    VAN = 'van', _('Van')
    SNOWBLOWER = 'snowblower', _('Snowblower')
    LAWNMOWER = 'lawnmower', _('Lawnmower')


class TrailerSubtypeChoice(models.TextChoices):
    ONBOARD = 'onboard', _('Onboard')
    CLOSED = 'closed', _('Closed')


class TrailerStatusChoice(models.TextChoices):
    AVAILABLE = 'available', _('Available')
    RENTED = 'rented', _('Rented')
    MAINTENANCE = 'maintenance', _('Under Maintenance')
    RESERVED = 'reserved', _('Reserved')
    WRITTEN_OFF = 'written_off', _('Written Off')
