from rest_framework_json_api import views
from rest_framework_json_api.utils import format_value


class FormatRelatedFieldMixin:
    """Fixes a bug where related fields are not formatted."""

    def dispatch(self, request, *args, **kwargs):
        if "related_field" in kwargs:
            kwargs["related_field"] = format_value(
                self.kwargs["related_field"], "underscore"
            )
        return super().dispatch(request, *args, **kwargs)


class ModelViewSet(FormatRelatedFieldMixin, views.ModelViewSet):
    pass


class ReadOnlyModelViewSet(FormatRelatedFieldMixin, views.ReadOnlyModelViewSet):
    pass


class RelationshipView(FormatRelatedFieldMixin, views.RelationshipView):
    pass
