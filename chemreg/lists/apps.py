from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ListsConfig(AppConfig):
    name = "chemreg.lists"
    verbose_name = _("Lists")

    def ready(self):
        try:
            import chemreg.lists.signals  # noqa F401
        except ImportError:
            pass
