from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommonConfig(AppConfig):
    name = "chemreg.common"
    verbose_name = _("Common")

    def ready(self):
        try:
            import chemreg.common.signals  # noqa F401
        except ImportError:
            pass
