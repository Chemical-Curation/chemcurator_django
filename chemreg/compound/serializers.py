from rest_framework import serializers

from chemreg.compound.models import (
    BaseCompound,
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)

# from rest_framework.validators import UniqueValidator


class BaseCompoundSerializer(serializers.ModelSerializer):
    """The base class for serializing compounds."""

    id = serializers.CharField(
        source="cid",
        validators=BaseCompound._meta.get_field("cid").validators,
        # + [UniqueValidator(queryset=BaseCompound.objects.all())], # this will fail tests
        required=False,
    )

    class Meta:
        model = BaseCompound
        fields = ("cid", "structure", "id")
        lookup_field = "cid"


class TypeSerializer(serializers.ModelSerializer):
    """Serializer to add the model type to the object."""

    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return self.Meta.model._meta.verbose_name


class DefinedCompoundSerializer(BaseCompoundSerializer, TypeSerializer):
    """The serializer for defined compounds."""

    class Meta:
        model = DefinedCompound
        fields = ("type", "id", "molefile", "inchikey")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["attributes"] = {
            "molfile-v3000": rep.pop("molefile"),
            "inchikey": rep.pop("inchikey"),
        }
        return rep


class QueryStructureTypeSerializer(serializers.ModelSerializer):
    """The serializer for query structure type."""

    class Meta:
        model = QueryStructureType
        fields = ("name", "label", "short_description", "long_description")


class IllDefinedCompoundSerializer(BaseCompoundSerializer, TypeSerializer):
    """The serializer for ill-defined compounds."""

    # query_structure_type = serializers.RelatedField(many=False, read_only=True)
    query_structure_type = QueryStructureTypeSerializer(many=False, required=False)

    class Meta:
        model = IllDefinedCompound
        fields = ("type", "id", "mrvfile", "query_structure_type")
