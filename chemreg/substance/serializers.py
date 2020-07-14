from chemreg.jsonapi.serializers import HyperlinkedModelSerializer
from chemreg.substance.models import SynonymType


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
