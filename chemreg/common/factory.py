import factory
from factory.base import BaseFactory, FactoryMetaClass
from rest_framework_json_api.renderers import JSONRenderer
from rest_framework_json_api.utils import (
    format_value,
    get_resource_type_from_serializer,
)


def is_relation(obj):
    if isinstance(obj, dict) and len(obj) == 2 and "type" in obj and "id" in obj:
        return True
    if isinstance(obj, list) and len(obj) and isinstance(dict, obj[0]):
        return is_relation(obj[0])
    return False


class DjangoSerializerFactoryMetaClass(FactoryMetaClass):
    """A shim to allow SubFactories to render correctly with JSON:API."""

    def __new__(mcs, class_name, bases, attrs):
        for field in attrs.values():
            if isinstance(field, factory.SubFactory):
                field.defaults["_is_sub_factory"] = True
        return super().__new__(mcs, class_name, bases, attrs)


class DjangoSerializerFactory(BaseFactory, metaclass=DjangoSerializerFactoryMetaClass):
    """A factory to make models via a serializer.

    This returns serializer objects. Additionally, it can render JSON POSTs.
    """

    class Meta:
        abstract = True

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        data = {k: v for k, v in kwargs.items() if k in cls._meta.model.Meta.fields}
        adjusted_kwargs = {k: v for k, v in kwargs.items() if k not in data}
        adjusted_kwargs["data"] = data
        return adjusted_kwargs

    @classmethod
    def _create_resource(cls, serializer_class, *args, **kwargs):
        """Make the resource object for related fields."""
        serializer = cls._create(serializer_class, *args, **kwargs)
        resource_type = get_resource_type_from_serializer(serializer_class)
        return {"type": resource_type, "id": str(serializer.instance.pk)}

    @classmethod
    def _build(cls, serializer_class, *args, **kwargs):
        """Build the serializer, but do not save to the database.

        If there is a related SubFactory, though, we must save it to the
        database in order to get the PK.
        """
        if kwargs.pop("_is_sub_factory", False):
            return cls._create_resource(serializer_class, *args, **kwargs)
        return serializer_class(*args, **kwargs)

    @classmethod
    def _create(cls, serializer_class, *args, **kwargs):
        """Build the serializer and save it to the database."""
        if kwargs.pop("_is_sub_factory", False):
            return cls._create_resource(serializer_class, *args, **kwargs)
        serializer = serializer_class(*args, **kwargs)
        serializer.is_valid()
        instance = serializer.save()
        return serializer_class(instance)

    @classmethod
    def json(cls, *args, **kwargs):
        """Render a JSON POST request."""
        serializer = cls.build(*args, **kwargs)
        attributes = {}
        relationships = {}
        for key, value in serializer.initial_data.items():
            if is_relation(value):
                relationships[format_value(key)] = {"data": value}
            else:
                attributes[format_value(key)] = value
        data = {"type": get_resource_type_from_serializer(serializer)}
        if attributes:
            data["attributes"] = attributes
        if relationships:
            data["relationships"] = relationships
        return JSONRenderer().render({"data": data})
