from chemreg.jsonapi.serializers import HyperlinkedModelSerializer
from chemreg.substance.models import QCLevelsType, Source, SubstanceType, SynonymType


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
