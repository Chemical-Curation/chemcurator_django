from rest_framework.exceptions import ValidationError

from chemreg.compound.models import BaseCompound
from chemreg.compound.serializers import CompoundSerializer
from chemreg.jsonapi.relations import (
    PolymorphicResourceRelatedField,
    ResourceRelatedField,
)
from chemreg.jsonapi.serializers import HyperlinkedModelSerializer
from chemreg.substance.models import (
    QCLevelsType,
    RelationshipType,
    Source,
    Substance,
    SubstanceType,
    SynonymQuality,
    SynonymType,
)


class QCLevelsTypeSerializer(HyperlinkedModelSerializer):
    """The serializer for QCLevelsType Types."""

    class Meta:
        model = QCLevelsType
        fields = [
            "name",
            "label",
            "short_description",
            "long_description",
            "rank",
        ]


class SynonymTypeSerializer(HyperlinkedModelSerializer):
    """The serializer for Synonym Types."""

    class Meta:
        model = SynonymType
        fields = [
            "name",
            "label",
            "short_description",
            "long_description",
            "validation_regular_expression",
            "score_modifier",
        ]


class SourceSerializer(HyperlinkedModelSerializer):
    """The serializer for Sources."""

    class Meta:
        model = Source
        fields = [
            "name",
            "label",
            "short_description",
            "long_description",
        ]


class SubstanceSerializer(HyperlinkedModelSerializer):
    """The serializer for Substances
    """

    included_serializers = {
        "source": "chemreg.substance.serializers.SourceSerializer",
        "substance_type": "chemreg.substance.serializers.SubstanceTypeSerializer",
        "qc_level": "chemreg.substance.serializers.QCLevelsTypeSerializer",
        "associated_compound": "chemreg.compound.serializers.CompoundSerializer",
    }

    source = ResourceRelatedField(queryset=Source.objects, model=Source)
    substance_type = ResourceRelatedField(
        queryset=SubstanceType.objects, model=SubstanceType
    )
    qc_level = ResourceRelatedField(queryset=QCLevelsType.objects, model=QCLevelsType)
    associated_compound = PolymorphicResourceRelatedField(
        polymorphic_serializer=CompoundSerializer,
        queryset=BaseCompound.objects,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Substance
        fields = [
            "sid",
            "preferred_name",
            "display_name",
            "description",
            "public_qc_note",
            "private_qc_note",
            "casrn",
            "source",
            "substance_type",
            "qc_level",
            "associated_compound",
        ]


class SubstanceTypeSerializer(HyperlinkedModelSerializer):
    """The serializer for Substance Types."""

    class Meta:
        model = SubstanceType
        fields = [
            "name",
            "label",
            "short_description",
            "long_description",
        ]


class RelationshipTypeSerializer(HyperlinkedModelSerializer):
    """The serializer for Substance Types."""

    class Meta:
        model = RelationshipType
        fields = [
            "name",
            "label",
            "short_description",
            "long_description",
            "corrolary_label",
            "corrolary_short_description",
        ]


class SynonymQualitySerializer(HyperlinkedModelSerializer):
    """The serializer for Synonym Qualities."""

    class Meta:
        model = SynonymQuality
        fields = [
            "name",
            "label",
            "short_description",
            "long_description",
            "score_weight",
            "is_restrictive",
        ]

    def validate_score_weight(self, value):
        if not value > 0:
            raise ValidationError("Score Weight must be greater than zero.")
        return value
