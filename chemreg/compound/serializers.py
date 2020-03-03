from rest_framework import serializers

from chemreg.compound.models import (
    BaseCompound,
    DefinedCompound,
    QueryStructureType,
    IllDefinedCompound,
)


class BaseCompoundSerializer(serializers.ModelSerializer):
    """The base class for serializing compounds."""

    id = serializers.CharField(
        source="cid", validators=BaseCompound._meta.get_field("cid").validators
    )

    class Meta:
        model = BaseCompound
        fields = ("id", "structure")


class DefinedCompoundSerializer(BaseCompoundSerializer):
    """The serializer for defined compounds."""

    class Meta:
        model = DefinedCompound
        fields = ("id", "molefile", "inchikey")


class IllDefinedCompoundSerializer(BaseCompoundSerializer):
    """The serializer for ill-defined compounds."""

    class Meta:
        model = IllDefinedCompound
        fields = ("id", "mrvfile", "query_structure_type")


class QueryStructureTypeSerializer(serializers.ModelSerializer):
    """The serializer for query structure type."""

    class Meta:
        model = QueryStructureType
        fields = ("name", "label", "short_description", "long_description")
