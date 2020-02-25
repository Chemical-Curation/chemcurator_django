import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Automatically fixes formatting issues and reports any other linting errors"

    def handle(self, *args, **options):
        subprocess.run(["isort", "--apply", "--quiet"], cwd=settings.ROOT_DIR)
        subprocess.run(["black", "--quiet", "."], cwd=settings.ROOT_DIR)
        subprocess.run(["flake8"], cwd=settings.ROOT_DIR)
