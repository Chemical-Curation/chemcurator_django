from rest_framework_json_api import relations
from rest_framework_json_api.utils import format_value


class FormatRelatedFieldMixin:
    """Fixes a bug where related fields are not formatted."""

    def get_url(self, name, view_name, kwargs, request):
        if "related_field" in kwargs:
            kwargs["related_field"] = format_value(kwargs["related_field"])
        return super().get_url(name, view_name, kwargs, request)


class AutoRelatedLinkMixin:
    """Allows related fields to get their links automatically."""

    @property
    def self_link_view_name(self):
        if self.read_only:
            return None
        return self.context["view"].basename + "-relationships"

    @property
    def related_link_view_name(self):
        return self.context["view"].basename + "-related"


class HyperlinkedRelatedField(
    AutoRelatedLinkMixin, FormatRelatedFieldMixin, relations.HyperlinkedRelatedField,
):
    pass


class ResourceRelatedField(
    AutoRelatedLinkMixin, FormatRelatedFieldMixin, relations.ResourceRelatedField,
):
    pass


class PolymorphicResourceRelatedField(
    AutoRelatedLinkMixin,
    FormatRelatedFieldMixin,
    relations.PolymorphicResourceRelatedField,
):
    pass


class SerializerMethodResourceRelatedField(
    AutoRelatedLinkMixin,
    FormatRelatedFieldMixin,
    relations.SerializerMethodResourceRelatedField,
):
    pass
