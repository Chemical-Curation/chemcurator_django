from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework_json_api.utils import format_value

from chemreg.compound.fields import StructureAliasField
from chemreg.compound.models import (
    BaseCompound,
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
)
from chemreg.compound.validators import (
    validate_inchikey_computable,
    validate_inchikey_unique,
    validate_molfile_v2000,
    validate_molfile_v3000_computable,
    validate_smiles,
)
from chemreg.indigo.inchi import get_inchikey
from chemreg.indigo.molfile import get_molfile_v3000
from chemreg.jsonapi.serializers import (
    HyperlinkedModelSerializer,
    PolymorphicModelSerializer,
)


class BaseCompoundSerializer(HyperlinkedModelSerializer):
    """The base serializer for compounds."""

    serializer_field_mapping = HyperlinkedModelSerializer.serializer_field_mapping
    serializer_field_mapping.update({StructureAliasField: serializers.CharField})


class DefinedCompoundSerializer(BaseCompoundSerializer):
    """The serializer for defined compounds."""

    molfile_v2000 = serializers.CharField(
        write_only=True,
        required=False,
        validators=[
            validate_molfile_v2000,
            validate_inchikey_computable,
            validate_molfile_v3000_computable,
        ],
        trim_whitespace=False,
    )
    smiles = serializers.CharField(
        write_only=True,
        required=False,
        validators=[
            validate_smiles,
            validate_inchikey_computable,
            validate_molfile_v3000_computable,
        ],
        trim_whitespace=False,
    )
    alt_structures = ("molfile_v2000", "molfile_v3000", "smiles")

    class Meta:
        model = DefinedCompound
        fields = (
            "cid",
            "inchikey",
            "molfile_v2000",
            "molfile_v3000",
            "smiles",
        )
        extra_kwargs = {"molfile_v3000": {"required": False, "trim_whitespace": False}}

    def __init__(self, *args, admin_override=False, **kwargs):
        if not admin_override:
            for structure in self.alt_structures:
                field = self.fields[structure]
                field.validators.append(validate_inchikey_unique)
        super().__init__(*args, **kwargs)

    def validate_cid(self, value):
        if "inchikey" not in self.initial_data:
            raise ValidationError("InchIKey must be included when CID is defined.")
        return value

    def validate_inchikey(self, value):
        if "cid" not in self.initial_data:
            raise ValidationError("CID must be included when InchIKey is defined.")
        return value

    def to_internal_value(self, data):
        matched_fields = set(self.alt_structures) & set(self.initial_data.keys())
        formatted_fields = [format_value(f) for f in sorted(self.alt_structures)]
        formatted_matched_fields = [format_value(f) for f in sorted(matched_fields)]
        if not matched_fields:
            raise ValidationError(
                {"non_field_errors": f"One of {sorted(formatted_fields)} required."}
            )
        if len(matched_fields) > 1:
            raise ValidationError(
                {
                    "non_field_errors": (
                        f"Only one of {formatted_fields} allowed. "
                        f"Recieved {formatted_matched_fields}."
                    )
                }
            )
        data = super().to_internal_value(data)  # calls field validators
        structure = next(k for k in self.alt_structures if k in data)
        data["molfile_v3000"] = get_molfile_v3000(data.pop(structure))
        if "inchikey" not in data:
            data["inchikey"] = get_inchikey(data["molfile_v3000"])
        return data


class DefinedCompoundDetailSerializer(DefinedCompoundSerializer):
    molecular_weight = serializers.SerializerMethodField()
    molecular_formula = serializers.SerializerMethodField()
    smiles = serializers.SerializerMethodField()
    calculated_inchikey = serializers.SerializerMethodField()

    class Meta(DefinedCompoundSerializer.Meta):
        fields = DefinedCompoundSerializer.Meta.fields + (
            "molecular_weight",
            "molecular_formula",
            "smiles",
            "calculated_inchikey",
        )

    def get_molecular_weight(self, obj):
        return obj.indigo_structure.molecularWeight()

    def get_molecular_formula(self, obj):
        return obj.indigo_structure.grossFormula()

    def get_smiles(self, obj):
        return obj.indigo_structure.smiles()

    def get_calculated_inchikey(self, obj):
        return get_inchikey(obj.molfile_v3000)


class QueryStructureTypeSerializer(HyperlinkedModelSerializer):
    """The serializer for query structure type."""

    class Meta:
        model = QueryStructureType
        fields = ("name", "label", "short_description", "long_description")


class IllDefinedCompoundSerializer(BaseCompoundSerializer):
    """The serializer for ill-defined compounds."""

    query_structure_type = QueryStructureTypeSerializer

    class Meta:
        model = IllDefinedCompound
        fields = ("cid", "mrvfile", "query_structure_type")


class CompoundSerializer(PolymorphicModelSerializer):
    """The serializer for both ill-defined and defined compounds."""

    polymorphic_serializers = [DefinedCompoundSerializer, IllDefinedCompoundSerializer]

    class Meta:
        model = BaseCompound
        fields = ["cid"]
