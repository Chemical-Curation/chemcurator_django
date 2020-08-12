from rest_framework.exceptions import ValidationError

from chemreg.common.serializers import ControlledVocabSerializer
from chemreg.common.validators import validate_casrn_checksum
from chemreg.compound.models import BaseCompound
from chemreg.compound.serializers import CompoundSerializer
from chemreg.jsonapi.relations import PolymorphicResourceRelatedField
from chemreg.jsonapi.serializers import HyperlinkedModelSerializer
from chemreg.substance.models import (
    QCLevelsType,
    RelationshipType,
    Source,
    Substance,
    SubstanceRelationship,
    SubstanceType,
    Synonym,
    SynonymQuality,
    SynonymType,
)


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
            "is_casrn",
        ]
        model = SynonymType

    def validate(self, data):
        # todo: validate the validation_regular_expression before validating checksum
        if self.instance and data.get("is_casrn"):
            self.validate_synonym_set_casrn_checksum()
        return data

    def validate_synonym_set_casrn_checksum(self):
        """This validates the checksum for CAS-RNs.

        This will need to be called after regex validation for self.validation_regular_expression
        as an additional non-regex check
        """
        failed_synonyms = []
        for synonym in self.instance.synonym_set.all():
            try:
                validate_casrn_checksum(synonym.identifier)
            except ValidationError:
                failed_synonyms.append(synonym)
        if failed_synonyms:
            raise ValidationError(
                "Synonyms with invalid CAS-RN checksums: ["
                f"{', '.join(syn.identifier for syn in failed_synonyms)}]",
                "invalid_data",
            )


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

    def validate(self, data):
        synonym_type = data.get("synonym_type", None) or self.instance.synonym_type
        # If the synonym type is casrn
        if synonym_type.is_casrn:
            # Verify that the identifier has a valid casrn checksum
            validate_casrn_checksum(data["identifier"])
        return data


class SubstanceRelationshipSerializer(HyperlinkedModelSerializer):
    """The serializer for Substance Relationships."""

    from_substance = SubstanceSerializer
    to_substance = SubstanceSerializer
    source = SourceSerializer
    relationship_type = RelationshipTypeSerializer

    class Meta:
        model = SubstanceRelationship
        fields = [
            "from_substance",
            "to_substance",
            "source",
            "relationship_type",
            "qc_notes",
        ]
