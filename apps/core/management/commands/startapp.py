import os
import shutil
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    """
    Служит для создания базового приложения.
    Для запуска: python manage.py startapp <Название приложения>
    """

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the application.")

    def _make_directory(self, path, name):
        directory = os.path.join(path, name)
        os.makedirs(directory, exist_ok=True)
        self._make_file(directory, "__init__.py")
        return directory

    def _make_file(self, path, name, content=None):
        open(os.path.join(path, name), "w").write(content if content else "\n")

    def _create_base_app(self, app_path, app_name):
        """Создание стандартного приложения"""

        os.makedirs(app_path)
        self._make_file(app_path, "models.py", "from django.db import models\n\n")

        apps_content = f"from django.apps import AppConfig\n\n\nclass {app_name.capitalize()}Config(AppConfig):\n\tdefault_auto_field = 'django.db.models.BigAutoField'\n\tname = 'apps.{app_name}'\n"
        self._make_file(app_path, "apps.py", apps_content)

        urls_content = f"from django.urls import path\nfrom apps.{app_name} import views\n\nurlpatterns = []\n"
        self._make_file(app_path, "urls.py", urls_content)

        self._make_file(app_path, "enums.py", "from django.db import models\n\n")

    def _create_api_dir(self, app_path):
        """Создание /api директории"""

        api_dir = self._make_directory(app_path, "api")
        self._make_file(api_dir, "filters.py")
        self._make_file(api_dir, "views.py")
        self._make_file(api_dir, "viewsets.py")
        self._make_file(
            api_dir,
            "serializers.py",
            "from restdoctor.rest_framework import serializers\n\n",
        )

    def _create_logic_dir(self, app_path):
        """Создание /logic директории"""

        logic_dir = self._make_directory(app_path, "logic")
        self._make_directory(logic_dir, "repositories")
        self._make_directory(logic_dir, "services")
        self._make_directory(logic_dir, "use_cases")

    def _create_admin_dir(self, app_path, app_name):
        """Создание /admin директории"""

        admin_model_dir = self._make_directory(app_path, "admin")

        self._make_file(
            admin_model_dir, "admin_model.py", "from django.contrib import admin\n"
        )
        self._make_file(
            admin_model_dir,
            "__init__.py",
            f"from apps.{app_name}.admin import admin_model\n",
        )

    def _create_migrations_dir(self, app_path):
        """Создание /migrations директории"""

        self._make_directory(app_path, "migrations")

    def _create_test_dir(self, app_path):
        """Создание /test директории"""

        test_dir = self._make_directory(app_path, "test")
        self._make_directory(test_dir, "factory")
        self._make_directory(test_dir, "fixture")

    def _add_app_to_installed_apps(self, app_name):
        """
        Добавляет новое приложение в INSTALLED_APPS settings.py
        """
        settings_file = os.path.join(settings.BASE_DIR, "config", "settings.py")
        if not os.path.exists(settings_file):
            self.stdout.write(self.style.WARNING("settings.py не найден"))
            return

        app_full_name = f"\t'apps.{app_name}',\n"

        with open(settings_file, "r") as f:
            lines = f.readlines()

        inside_installed_apps = False
        for i, line in enumerate(lines):
            if line.strip().startswith("INSTALLED_APPS"):
                inside_installed_apps = True
            if inside_installed_apps and line.strip().startswith("]"):
                if any(f"apps.{app_name}" in l for l in lines):
                    return
                lines.insert(i, app_full_name)
                break

        with open(settings_file, "w") as f:
            f.writelines(lines)

    def handle(self, *args, **options):
        app_name = options["name"]
        apps_dir = os.path.join(settings.BASE_DIR, "apps")

        if not os.path.exists(apps_dir):
            os.makedirs(apps_dir)
            open(os.path.join(apps_dir, "__init__.py"), "w").close()

        app_path = os.path.join(apps_dir, app_name)
        if os.path.exists(app_path):
            raise CommandError(f"Приложение '{app_name}' уже существует в apps/")

        try:
            self._create_base_app(app_path, app_name)
            self._create_admin_dir(app_path, app_name)
            self._create_migrations_dir(app_path)
            self._create_api_dir(app_path)
            self._create_logic_dir(app_path)
            self._create_test_dir(app_path)

            self._add_app_to_installed_apps(app_name)

            self.stdout.write(
                self.style.SUCCESS(f"Приложение '{app_name}' успешно создано")
            )
        except Exception as e:
            if os.path.exists(app_path):
                shutil.rmtree(app_path)
            raise CommandError(f"Ошибка при создании приложения: {e}")
