from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CompoundConfig(AppConfig):
    name = "chemreg.compound"
    verbose_name = _("Compound")

    def ready(self):
        try:
            import chemreg.compound.signals  # noqa F401
        except ImportError:
            pass
