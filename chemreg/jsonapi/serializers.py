import inspect
from collections import ChainMap

from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.related import RelatedField
from django.db.models.query import QuerySet
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


class AutoIncludeMetaclass(serializers.SerializerMetaclass):
    """
    This metaclass sets a dictionary named `included_serializers` on the class if not explicitly declared.

    Any instances of `ModelSerializer`, `HyperlinkedModelSerializer`,  `PolymorphicModelSerializer`,
    or a string pointing to a subclass of these included as attributes on either the class or on any
    of its superclasses will be included in the `included_serializers` dictionary.
    """

    @classmethod
    def _get_included_serializers(cls, bases, attrs):
        """Find serializers included on the serializer"""

        included_serializers = {}
        meta = attrs.get("Meta", None)
        model = getattr(meta, "model", None)
        for field_name, field_obj in list(attrs.items()):
            try:
                model_field = model._meta.get_field(field_name)
            except (AttributeError, FieldDoesNotExist):
                model_field = None
            # Does this field point to a RelatedField on the model?
            is_related_field = isinstance(model_field, RelatedField)
            # Is this possibly an import string?
            is_string = isinstance(field_obj, str)
            # Is this an accepted serializer?
            is_serializer = inspect.isclass(field_obj) and issubclass(
                field_obj,
                (
                    serializers.ModelSerializer,
                    serializers.HyperlinkedModelSerializer,
                    serializers.PolymorphicModelSerializer,
                ),
            )
            if is_related_field and (is_string or is_serializer):
                included_serializer = attrs.pop(field_name)
                included_serializers[field_name] = included_serializer
        # Gather the included serializers from all bases
        base_included_serializer_dicts = [
            serializer.included_serializers
            for serializer in bases
            if hasattr(serializer, "included_serializers")
            and serializer.included_serializers
        ]
        if included_serializers:
            return ChainMap(included_serializers, *base_included_serializer_dicts)
        return ChainMap(*base_included_serializer_dicts)

    def __new__(cls, name, bases, attrs):
        if "included_serializers" not in attrs:
            attrs["included_serializers"] = cls._get_included_serializers(bases, attrs)
        return super().__new__(cls, name, bases, attrs)


class PolymorphicAutoIncludeMetaclass(
    AutoIncludeMetaclass, serializers.PolymorphicSerializerMetaclass
):
    """
    This metaclass sets a dictionary named `included_serializers` on the class if not explicitly declared.

    The `included_serializers` will be a combination of every `included_serializers` included
    in the list of each `polymorphic_serializers`.
    """

    @classmethod
    def _get_included_serializers(cls, bases, attrs):
        """Find serializers included on the polymorphic serializer."""

        polymorphic_serializers = attrs.get("polymorphic_serializers", [])
        polymorphic_included_serializer_dicts = [
            serializer.included_serializers
            for serializer in polymorphic_serializers
            if hasattr(serializer, "included_serializers")
            and serializer.included_serializers
        ]
        base_included_serializer_dicts = [
            serializer.included_serializers
            for serializer in bases
            if hasattr(serializer, "included_serializers")
            and serializer.included_serializers
        ]
        return ChainMap(
            *polymorphic_included_serializer_dicts, *base_included_serializer_dicts
        )

    def __new__(cls, name, bases, attrs):

        # There's a bug in the base serializers.PolymorphicSerializerMetaclass that prevents
        # subclassing it.
        if name == "PolymorphicModelSerializer":
            return super(serializers.PolymorphicSerializerMetaclass, cls).__new__(
                cls, name, bases, attrs
            )
        return super().__new__(cls, name, bases, attrs)


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
        # Todo:  This was originally to fix a bug with the compounds endpoint
        #  where the defined/ill-defined compounds were breaking.  It is also
        #  preventing related links from populating with their serializers.
        # if hasattr(self, "context") and "view" in self.context:
        #     basename = self.context["view"].basename
        #     field_class = self.serializer_url_field
        #     field_kwargs = {"view_name": f"{basename}-detail"}
        #     return (field_class, field_kwargs)
        return super().build_url_field(field_name, model_class)


class PolymorphicInitKwargMixin:
    """Fixes a bug where init kwargs are not passed to child serializers."""

    serializer_kwargs = {}

    def __init__(self, *args, **kwargs):
        self._init_kwarg_values = {}
        for kwarg_list in self.serializer_kwargs.values():
            for kwarg in kwarg_list:
                if kwarg in kwargs:
                    self._init_kwarg_values[kwarg] = kwargs.pop(kwarg)
        super().__init__(*args, **kwargs)

    def get_serializer_kwargs(self, instance):
        serializer_class = self.get_polymorphic_serializer_for_instance(instance)
        serializer_kwarg_list = self.serializer_kwargs.get(serializer_class, [])
        serializer_kwargs = {}
        for kwarg in serializer_kwarg_list:
            if kwarg in self._init_kwarg_values:
                serializer_kwargs[kwarg] = self._init_kwarg_values[kwarg]
        return serializer_kwargs

    def to_representation(self, instance):
        serializer_class = self.get_polymorphic_serializer_for_instance(instance)
        serializer_kwargs = self.get_serializer_kwargs(instance)
        return serializer_class(
            instance, context=self.context, **serializer_kwargs
        ).to_representation(instance)

    def get_fields(self):
        if self.instance not in (None, []):
            if not isinstance(self.instance, QuerySet):
                serializer_class = self.get_polymorphic_serializer_for_instance(
                    self.instance
                )
                serializer_kwargs = self.get_serializer_kwargs(self.instance)
                return serializer_class(
                    self.instance, context=self.context, **serializer_kwargs
                ).get_fields()
            else:
                raise Exception(
                    "Cannot get fields from a polymorphic serializer given a queryset"
                )
        return super().get_fields()


class HyperlinkedModelSerializer(
    ResourceRelatedFieldMixin,
    PolymorphicSelfLinkMixin,
    serializers.HyperlinkedModelSerializer,
    SelfLinkMixin,
    RootMetaMixin,
    metaclass=AutoIncludeMetaclass,
):
    pass


class ModelSerializer(
    ResourceRelatedFieldMixin,
    PolymorphicSelfLinkMixin,
    serializers.ModelSerializer,
    SelfLinkMixin,
    RootMetaMixin,
    metaclass=AutoIncludeMetaclass,
):
    pass


class PolymorphicModelSerializer(
    PolymorphicInitKwargMixin,
    ModelSerializer,
    serializers.PolymorphicModelSerializer,
    metaclass=PolymorphicAutoIncludeMetaclass,
):
    pass
