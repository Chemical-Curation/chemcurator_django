from rest_framework_json_api import serializers


class RootMetaMixin:
    """Adds API version to the responses."""

    def get_root_meta(self, *args, **kwargs):
        "Adds the API version"
        return {"apiVersion": "1.0.0-beta"}


class HyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer, RootMetaMixin):
    pass


class ModelSerializer(serializers.ModelSerializer, RootMetaMixin):
    pass


class PolymorphicModelSerializer(
    type(
        "PolymorphicModelSerializerBase",
        serializers.PolymorphicModelSerializer.__bases__,
        dict(vars(serializers.PolymorphicModelSerializer)),
    ),
    RootMetaMixin,
    metaclass=serializers.PolymorphicSerializerMetaclass,
):
    pass
