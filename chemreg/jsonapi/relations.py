from rest_framework_json_api import relations
from rest_framework_json_api.utils import format_value


class FormatRelatedFieldMixin:
    """Fixes a bug where related fields are not formatted."""

    def get_url(self, name, view_name, kwargs, request):
        if "related_field" in kwargs:
            kwargs["related_field"] = format_value(kwargs["related_field"])
        return super().get_url(name, view_name, kwargs, request)


class HyperlinkedRelatedField(
    FormatRelatedFieldMixin, relations.HyperlinkedRelatedField
):
    pass


class ResourceRelatedField(FormatRelatedFieldMixin, relations.ResourceRelatedField):
    pass


class PolymorphicResourceRelatedField(
    FormatRelatedFieldMixin, relations.PolymorphicResourceRelatedField
):
    pass


class SerializerMethodResourceRelatedField(
    FormatRelatedFieldMixin, relations.SerializerMethodResourceRelatedField
):
    pass
