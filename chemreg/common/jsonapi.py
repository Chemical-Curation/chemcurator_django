from rest_framework_json_api import pagination, serializers


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


class HyperlinkedModelSerializer(
    serializers.HyperlinkedModelSerializer, SelfLinkMixin, RootMetaMixin
):
    pass


class ModelSerializer(serializers.ModelSerializer, SelfLinkMixin, RootMetaMixin):
    pass


class PolymorphicModelSerializer(
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


class JsonApiPageNumberPagination(pagination.JsonApiPageNumberPagination):
    max_page_size = 1000
