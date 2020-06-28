from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SubstanceConfig(AppConfig):
    name = "chemreg.substance"
    verbose_name = _("Substance")

    def ready(self):
        try:
            import chemreg.substance.signals  # noqa F401
        except ImportError:
            pass
