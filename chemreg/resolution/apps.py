from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ResolutionConfig(AppConfig):
    name = "chemreg.resolution"
    verbose_name = _("Resolution")

    def ready(self):
        try:
            import chemreg.resolution.signals  # noqa F401
        except ImportError:
            pass
