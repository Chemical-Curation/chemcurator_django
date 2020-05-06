import inspect

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
        if "url" not in cls.Meta.fields:
            cls.Meta.fields += type(cls.Meta.fields)(("url",))
        return super().__new__(cls, *args, **kwargs)


class AutoRelatedMixin:
    """Pulls in related fields from serializer."""

    def __new__(cls, *args, **kwargs):
        included_serializers = {
            key: val
            for key, val in cls.__dict__.items()
            if key in cls.Meta.fields
            and inspect.isclass(val)
            and issubclass(val, serializers.ModelSerializer)
        }
        for key in included_serializers:
            delattr(cls, key)
        if included_serializers:
            if not hasattr(cls, "included_serializers"):
                cls.included_serializers = included_serializers
            else:
                cls.included_serializers = cls.included_serializers.update(
                    included_serializers
                )
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


class PolymorphicModelSerializer(
    ResourceRelatedFieldMixin,
    AutoRelatedMixin,
    type(
        "PolymorphicModelSerializerBase",
        serializers.PolymorphicModelSerializer.__bases__,
        dict(vars(serializers.PolymorphicModelSerializer)),
    ),
    SelfLinkMixin,
    RootMetaMixin,
    metaclass=serializers.PolymorphicSerializerMetaclass,
):
    pass
