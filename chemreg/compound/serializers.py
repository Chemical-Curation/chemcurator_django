from indigo import Indigo
from rest_framework_json_api.relations import ResourceRelatedField

from chemreg.common import jsonapi
from chemreg.compound.models import (
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)
from chemreg.compound.validators import validate_inchikey_unique, validate_smiles


class DefinedCompoundSerializer(jsonapi.HyperlinkedModelSerializer):
    """The serializer for defined compounds."""

    class Meta:
        model = DefinedCompound
        fields = (
            "cid",
            "molfile_v3000",
            "inchikey",
        )
        extra_kwargs = {
            "molfile_v3000": {"style": {"base_template": "textarea.html", "rows": 10}},
            "override": {"write_only": True, "style": {"base_template": "radio.html"}},
            "smiles": {
                "write_only": True,
                "style": {"base_template": "textarea.html", "rows": 5},
            },
        }

    def to_internal_value(self, data):
        if data.get("smiles"):  # if the json contains a SMILES value...
            smiles = data["smiles"]  # ...assign it to a local var
            validate_smiles(smiles)
            indigo = Indigo()
            indigo.setOption("molfile-saving-mode", "3000")
            struct = indigo.loadStructure(structureStr=smiles,)  # ...create a structure
            data["molfile_v3000"] = struct.molfile()  # store in molfile_v3000
        else:
            pass
        return super().to_internal_value(data)

    def validate(self, attrs):
        if not self.initial_data.get("override"):  # validate uniqueness of inchikey
            validate_inchikey_unique(self.initial_data["molfile_v3000"])
        return attrs


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
