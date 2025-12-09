from django.db import models


class LanguageChoice(models.TextChoices):
    RU = "ru"
    EN = "en"
    LV = "lv"


class LegalChoice(models.TextChoices):
    YES = "yes"
    NO = "no"
    DEL = "del"

