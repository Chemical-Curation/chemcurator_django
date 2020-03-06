from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UtilsConfig(AppConfig):
    name = "chemreg.utils"
    verbose_name = _("Utils")

    def ready(self):
        try:
            import chemreg.utils.signals  # noqa F401
        except ImportError:
            pass
