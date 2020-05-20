from rest_framework import serializers

from chemreg.common.validators import OneOfValidator
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
from rest_framework_json_api.relations import PolymorphicResourceRelatedField


class BaseCompoundSerializer(HyperlinkedModelSerializer):
    """The base serializer for compounds."""

    serializer_field_mapping = HyperlinkedModelSerializer.serializer_field_mapping
    serializer_field_mapping.update({StructureAliasField: serializers.CharField})
    replaced_by = "chemreg.compound.serializers.CompoundSerializer"


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

    class Meta:
        model = DefinedCompound
        fields = (
            "cid",
            "inchikey",
            "molfile_v2000",
            "molfile_v3000",
            "smiles",
            "replaced_by",
        )
        extra_kwargs = {"molfile_v3000": {"required": False, "trim_whitespace": False}}
        validators = [
            OneOfValidator("molfile_v2000", "molfile_v3000", "smiles", required=True)
        ]

    def __init__(self, *args, admin_override=False, **kwargs):
        if not admin_override:
            for structrue in ("molfile_v2000", "molfile_v3000", "smiles"):
                field = self.fields[structrue]
                field.validators.append(validate_inchikey_unique)
        super().__init__(*args, **kwargs)

    def validate(self, data):
        alt_structures = ("molfile_v2000", "molfile_v3000", "smiles")
        alt_structure = next(k for k in alt_structures if k in data)
        data["molfile_v3000"] = get_molfile_v3000(data.pop(alt_structure))
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
        fields = ["cid", "mrvfile", "query_structure_type", "replaced_by"]


class ReplacementCompoundSerializer(PolymorphicModelSerializer):
    """The serializer for the replaced_by field in a compound, either defined or ill-defined."""

    polymorphic_serializers = [DefinedCompoundSerializer, IllDefinedCompoundSerializer]

    class Meta:
        model = BaseCompound
        fields = ["cid"]


class CompoundSerializer(PolymorphicModelSerializer):
    """The serializer for both ill-defined and defined compounds."""

    polymorphic_serializers = [DefinedCompoundSerializer, IllDefinedCompoundSerializer]
    replaced_by = PolymorphicResourceRelatedField(
        polymorphic_serializer=ReplacementCompoundSerializer,
        queryset=BaseCompound.objects.all(),
    )

    class Meta:
        model = BaseCompound
        fields = ["cid"]
