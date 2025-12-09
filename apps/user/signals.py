from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.user.models import User
from config.settings import env
import logging

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name == "apps.user":
        phone_code = env("SUPERUSER_PHONE_CODE")
        phone = env("SUPERUSER_PHONE")
        password = env("SUPERUSER_PASSWORD")

        if phone and phone_code and password:
            if not User.objects.filter(phone=phone).exists():
                logger.info("Creating superuser...")
                User.objects.create_superuser(phone=phone, password=password, phone_code=phone_code)
                logger.info("Superuser created successfully!")
