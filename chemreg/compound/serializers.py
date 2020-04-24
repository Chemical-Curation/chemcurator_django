from rest_framework_json_api.relations import ResourceRelatedField

from chemreg.common import jsonapi
from chemreg.compound.models import (
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)
from chemreg.compound.validators import (
    validate_inchikey_unique,
    validate_molfile_v2000,
    validate_single_structure,
    validate_smiles,
    validate_structure,
)
from chemreg.indigo.inchi import load_structure


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
            "molfile_v2000": {"style": {"base_template": "textarea.html", "rows": 10}},
        }

    def to_internal_value(self, data):
        if data.keys():  # False will pass on to *required
            validate_single_structure(data.keys())
        if data.get("smiles"):  # if the json contains a SMILES value...
            compound = data["smiles"]  # ...assign it to a local var
            validate_smiles(compound)
        elif data.get("molfile_v2000"):  # if the json contains a molfile_v2000 value...
            compound = str(data["molfile_v2000"])  # ...assign it to a local var
            validate_molfile_v2000(compound)
        else:
            return super().to_internal_value(data)
        validate_structure(compound)
        struct = load_structure(compound)
        data["molfile_v3000"] = struct.molfile()  # store in molfile_v3000
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
