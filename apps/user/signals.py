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
        email = env("SUPERUSER_EMAIL")
        first_name = env('SUPERUSER_FIRST_NAME')
        telegram = env('SUPERUSER_TELEGRAM')

        if phone and password and phone_code and email and first_name and telegram:
            if not User.objects.filter(phone=phone).exists():
                logger.info("Creating superuser...")
                User.objects.create_superuser(
                    phone=phone, password=password,
                    phone_code=phone_code,
                    email=email,
                    first_name=first_name,
                    telegram=telegram
                )
                logger.info("Superuser created successfully!")
