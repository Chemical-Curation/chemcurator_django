from rest_framework.exceptions import ValidationError

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


class ValidatePostParamsMixin:
    """return 400 if query parameter is not allowed in `post_query_params`"""

    def get_valid_post_query_params(self):
        if hasattr(self, "valid_post_query_params"):
            return self.valid_post_query_params
        else:
            return []

    def create(self, request, *args, **kwargs):
        for qp in request.query_params.keys():
            if qp not in self.get_valid_post_query_params():
                raise ValidationError("invalid query parameter: {}".format(qp))
        return super().create(request, *args, **kwargs)


class ModelViewSet(
    ValidatePostParamsMixin, FormatRelatedFieldMixin, views.ModelViewSet
):
    pass


class ReadOnlyModelViewSet(FormatRelatedFieldMixin, views.ReadOnlyModelViewSet):
    pass


class RelationshipView(FormatRelatedFieldMixin, views.RelationshipView):
    pass
