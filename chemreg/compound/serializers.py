from rest_framework_json_api import serializers

from chemreg.compound.models import (
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)


class DefinedCompoundSerializer(serializers.ModelSerializer):
    """The serializer for defined compounds."""

    class Meta:
        model = DefinedCompound
        fields = ("cid", "molfile_v3000", "inchikey")
        extra_kwargs = {
            "molfile_v3000": {"style": {"base_template": "textarea.html", "rows": 10}}
        }


class IllDefinedCompoundSerializer(serializers.ModelSerializer):
    """The serializer for ill-defined compounds."""

    included_serializers = {
        "query_structure_type": "chemreg.compound.serializers.QueryStructureTypeSerializer",
    }

    class Meta:
        model = IllDefinedCompound
        fields = ("cid", "mrvfile", "query_structure_type")

    class JSONAPIMeta:
        included_resources = ["query_structure_type"]


class QueryStructureTypeSerializer(serializers.ModelSerializer):
    """The serializer for query structure type."""

    class Meta:
        model = QueryStructureType
        fields = ("name", "label", "short_description", "long_description")
