from rest_framework_json_api.relations import ResourceRelatedField

from chemreg.common import jsonapi
from chemreg.compound.models import (
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)


class DefinedCompoundSerializer(jsonapi.HyperlinkedModelSerializer):
    """The serializer for defined compounds."""

    class Meta:
        model = DefinedCompound
        fields = ("cid", "molfile_v3000", "inchikey")
        extra_kwargs = {
            "molfile_v3000": {"style": {"base_template": "textarea.html", "rows": 10}}
        }


class IllDefinedCompoundSerializer(jsonapi.HyperlinkedModelSerializer):
    """The serializer for ill-defined compounds."""

    query_structure_type = ResourceRelatedField(
        queryset=QueryStructureType.objects,
        related_link_view_name="ill-defined-compounds-related",
        required=False,
        self_link_view_name="ill-defined-compounds-relationships",
    )

    included_serializers = {
        "query_structure_type": "chemreg.compound.serializers.QueryStructureTypeSerializer",
    }

    class Meta:
        model = IllDefinedCompound
        fields = ("cid", "mrvfile", "query_structure_type")


class QueryStructureTypeSerializer(jsonapi.HyperlinkedModelSerializer):
    """The serializer for query structure type."""

    class Meta:
        model = QueryStructureType
        fields = ("name", "label", "short_description", "long_description")
