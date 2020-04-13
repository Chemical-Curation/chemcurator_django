from rest_framework.exceptions import ParseError

import partialsmiles as ps
from indigo import Indigo
from rest_framework_json_api.relations import ResourceRelatedField

from chemreg.common import jsonapi
from chemreg.compound.models import (
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)
from chemreg.compound.validators import validate_smiles


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
            "smiles": {
                "write_only": True,
                "style": {"base_template": "textarea.html", "rows": 5},
            },
        }

    def to_internal_value(self, data):
        if data.get("smiles"):  # if the json contains a SMILES value...
            smiles = data["smiles"]  # ...assign it to a local var
            try:
                validate_smiles(smiles)
                indigo = Indigo()
                indigo.setOption("molfile-saving-mode", "3000")
                struct = indigo.loadStructure(
                    structureStr=smiles,
                )  # ...create a structure from it
                data[
                    "molfile_v3000"
                ] = struct.molfile()  # store the structure in the molfile_v3000 field
            except ps.SMILESSyntaxError as e:
                # the SMILES is invalid
                message = f"The SMILES string cannot be converted to a molfile.\n {e}"
                raise ParseError({"smiles": message})
        else:
            pass
        return super().to_internal_value(data)


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
