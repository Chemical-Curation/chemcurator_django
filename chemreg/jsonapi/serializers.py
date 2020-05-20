import copy

from django.utils.module_loading import import_string

from rest_framework_json_api import serializers

from chemreg.jsonapi.relations import ResourceRelatedField


class RootMetaMixin:
    """Adds API version to the responses."""

    def get_root_meta(self, *args, **kwargs):
        "Adds the API version"
        return {"apiVersion": "1.0.0-beta"}


class SelfLinkMixin:
    """Adds a link to "self" for a serializer."""

    def __new__(cls, *args, **kwargs):
        if hasattr(cls.Meta, "fields") and "url" not in cls.Meta.fields:
            cls.Meta.fields += type(cls.Meta.fields)(("url",))
        return super().__new__(cls, *args, **kwargs)


class AutoRelatedMixin:
    """Pulls in related fields from serializer."""

    @staticmethod
    def _gen_included_serializers(serializer):
        included_serializers = {}
        for fieldname in serializer.Meta.fields:
            field = getattr(serializer, fieldname, None)
            if isinstance(field, str):
                related_serializer = import_string(field)
            else:
                related_serializer = field
            if related_serializer and issubclass(
                related_serializer,
                (
                    serializers.ModelSerializer,
                    serializers.HyperlinkedModelSerializer,
                    serializers.PolymorphicModelSerializer,
                ),
            ):
                included_serializers[fieldname] = related_serializer

        return included_serializers

    def __new__(cls, *args, **kwargs):
        included_serializers = cls._gen_included_serializers(cls)
        for key in included_serializers:
            try:
                delattr(cls, key)
            except AttributeError:
                pass
        for serializer in getattr(cls, "polymorphic_serializers", []):
            included_serializers.update(cls._gen_included_serializers(serializer))
        if included_serializers:
            if not getattr(cls, "included_serializers", None):
                cls.included_serializers = included_serializers
            else:
                cls.included_serializers.update(included_serializers)
        return super().__new__(cls, *args, **kwargs)


class ResourceRelatedFieldMixin:
    """Mixes in the custom ResourceRelatedField."""

    serializer_related_field = ResourceRelatedField


class HyperlinkedModelSerializer(
    ResourceRelatedFieldMixin,
    AutoRelatedMixin,
    serializers.HyperlinkedModelSerializer,
    SelfLinkMixin,
    RootMetaMixin,
):
    pass


class ModelSerializer(
    ResourceRelatedFieldMixin,
    AutoRelatedMixin,
    serializers.ModelSerializer,
    SelfLinkMixin,
    RootMetaMixin,
):
    pass


PolymorphicSerializerMetaclass = serializers.PolymorphicSerializerMetaclass
PolymorphicModelSerializer = copy.deepcopy(serializers.PolymorphicModelSerializer)
PolymorphicModelSerializer.__bases__ = (ModelSerializer,)
PolymorphicModelSerializer.get_root_meta = RootMetaMixin.get_root_meta
