from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthConfig(AppConfig):
    name = "chemreg.auth"
    verbose_name = _("Authentication")
    label = "chemreg.auth"

    def ready(self):
        try:
            import chemreg.auth.signals  # noqa F401
        except ImportError:
            pass
