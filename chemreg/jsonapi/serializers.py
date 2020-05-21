import copy
import inspect

from django.utils.module_loading import import_string
from rest_framework.utils.field_mapping import get_relation_kwargs

from rest_framework_json_api import serializers

from chemreg.jsonapi.relations import (
    PolymorphicResourceRelatedField,
    ResourceRelatedField,
)


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


class AutoRelatedMetaclass(serializers.SerializerMetaclass):
    """Pulls in related fields from serializer."""

    def __new__(cls, name, bases, attrs):
        # Automatically include serializer
        included_serializers = attrs.get("included_serializers", {})
        # Inspect bases for their included serializers
        for base in bases:
            base_included_serializer = getattr(base, "included_serializers", {})
            for key, value in base_included_serializer.items():
                # Only include if not overwritten
                if key not in included_serializers:
                    included_serializers[key] = value
        for fieldname in getattr(attrs.get("Meta"), "fields", []):
            if fieldname not in included_serializers:
                field = attrs.get(fieldname)
                if (
                    isinstance(field, str)
                    or inspect.isclass(field)
                    and issubclass(
                        field,
                        (
                            serializers.ModelSerializer,
                            serializers.HyperlinkedModelSerializer,
                            serializers.PolymorphicModelSerializer,
                        ),
                    )
                ):
                    included_serializers[fieldname] = field
        attrs["included_serializers"] = included_serializers
        # Let DRF handle generating the fields
        for fieldname in included_serializers:
            if fieldname in attrs:
                attrs.pop(fieldname)
        return super(AutoRelatedMetaclass, cls).__new__(cls, name, bases, attrs)


class AutoIncludePolymorphicMixin:
    """Pulls in included fields from polymorphic serializers."""

    def __new__(cls, *args, **kwargs):
        included_serializers = getattr(cls, "included_serializers", None) or {}
        polymorphic_serializers = getattr(cls, "polymorphic_serializers", None) or []
        for serializer in polymorphic_serializers:
            serializer_included_serializers = (
                getattr(serializer, "included_serializers", None) or {}
            )
            included_serializers.update(serializer_included_serializers)
        cls.included_serializers = included_serializers
        return super().__new__(cls, *args, **kwargs)


class ResourceRelatedFieldMixin:
    """Mixes in the custom ResourceRelatedField/PolymorphicResourceRelatedField."""

    serializer_related_field = ResourceRelatedField

    def build_relational_field(self, field_name, relation_info):
        if field_name in self.included_serializers:
            serializer = self.included_serializers[field_name]
            if isinstance(serializer, str):
                serializer = import_string(serializer)
            if issubclass(serializer, serializers.PolymorphicModelSerializer):
                field_class = PolymorphicResourceRelatedField
                field_kwargs = get_relation_kwargs(field_name, relation_info)
                field_kwargs.pop("view_name")
                field_kwargs["polymorphic_serializer"] = serializer
                return (field_class, field_kwargs)
        return super().build_relational_field(field_name, relation_info)


class PolymorphicSelfLinkMixin:
    """Fixes a bug where polymorphic serializers return the wrong self link."""

    def build_url_field(self, field_name, model_class):
        if hasattr(self, "context") and "view" in self.context:
            basename = self.context["view"].basename
            field_class = self.serializer_url_field
            field_kwargs = {"view_name": f"{basename}-detail"}
            return (field_class, field_kwargs)
        return super().build_url_field(field_name, model_class)


class HyperlinkedModelSerializer(
    ResourceRelatedFieldMixin,
    PolymorphicSelfLinkMixin,
    serializers.HyperlinkedModelSerializer,
    SelfLinkMixin,
    RootMetaMixin,
    metaclass=AutoRelatedMetaclass,
):
    pass


class ModelSerializer(
    AutoIncludePolymorphicMixin,
    PolymorphicSelfLinkMixin,
    ResourceRelatedFieldMixin,
    serializers.ModelSerializer,
    SelfLinkMixin,
    RootMetaMixin,
    metaclass=AutoRelatedMetaclass,
):
    pass


PolymorphicModelSerializer = copy.deepcopy(serializers.PolymorphicModelSerializer)
PolymorphicModelSerializer.__bases__ = (ModelSerializer,)
PolymorphicModelSerializer.get_root_meta = RootMetaMixin.get_root_meta
