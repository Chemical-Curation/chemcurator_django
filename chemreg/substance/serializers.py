from rest_framework.exceptions import ValidationError

from chemreg.compound.models import BaseCompound
from chemreg.compound.serializers import CompoundSerializer
from chemreg.jsonapi.relations import PolymorphicResourceRelatedField
from chemreg.jsonapi.serializers import HyperlinkedModelSerializer
from chemreg.substance.models import (
    ControlledVocabulary,
    QCLevelsType,
    RelationshipType,
    Source,
    Substance,
    SubstanceType,
    Synonym,
    SynonymQuality,
    SynonymType,
)


class ControlledVocabSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ControlledVocabulary
        fields = [
            "name",
            "label",
            "short_description",
            "long_description",
            "deprecated",
        ]
        abstract = True


class QCLevelsTypeSerializer(ControlledVocabSerializer):
    """The serializer for QCLevelsType Types."""

    class Meta(ControlledVocabSerializer.Meta):
        fields = ControlledVocabSerializer.Meta.fields + [
            "rank",
        ]
        model = QCLevelsType


class SynonymTypeSerializer(ControlledVocabSerializer):
    """The serializer for Synonym Types."""

    class Meta(ControlledVocabSerializer.Meta):
        fields = ControlledVocabSerializer.Meta.fields + [
            "validation_regular_expression",
            "score_modifier",
        ]
        model = SynonymType


class SourceSerializer(ControlledVocabSerializer):
    """The serializer for Sources."""

    class Meta(ControlledVocabSerializer.Meta):
        model = Source


class SubstanceTypeSerializer(ControlledVocabSerializer):
    """The serializer for Substance Types."""

    class Meta(ControlledVocabSerializer.Meta):
        model = SubstanceType


class SubstanceSerializer(HyperlinkedModelSerializer):
    """The serializer for Substances."""

    included_serializers = {
        "source": "chemreg.substance.serializers.SourceSerializer",
        "substance_type": "chemreg.substance.serializers.SubstanceTypeSerializer",
        "qc_level": "chemreg.substance.serializers.QCLevelsTypeSerializer",
        "associated_compound": "chemreg.compound.serializers.CompoundSerializer",
    }

    source = SourceSerializer
    substance_type = SubstanceTypeSerializer
    qc_level = QCLevelsTypeSerializer
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


class RelationshipTypeSerializer(ControlledVocabSerializer):
    """The serializer for Substance Types."""

    class Meta(ControlledVocabSerializer.Meta):
        model = RelationshipType
        fields = ControlledVocabSerializer.Meta.fields + [
            "corrolary_label",
            "corrolary_short_description",
        ]


class SynonymQualitySerializer(ControlledVocabSerializer):
    """The serializer for Synonym Qualities."""

    class Meta(ControlledVocabSerializer.Meta):
        model = SynonymQuality
        fields = ControlledVocabSerializer.Meta.fields + [
            "score_weight",
            "is_restrictive",
        ]

    def validate_score_weight(self, value):
        if not value > 0:
            raise ValidationError("Score Weight must be greater than zero.")
        return value


class SynonymSerializer(HyperlinkedModelSerializer):
    """The serializer for Synonyms."""

    source = SourceSerializer
    substance = SubstanceSerializer
    synonym_quality = SynonymQualitySerializer
    synonym_type = SynonymTypeSerializer

    class Meta:
        model = Synonym
        fields = [
            "identifier",
            "qc_notes",
            "source",
            "substance",
            "synonym_quality",
            "synonym_type",
        ]
