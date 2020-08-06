from chemreg.common.serializers import ControlledVocabSerializer
from chemreg.lists.models import IdentifierType, ListType


class ListTypeSerializer(ControlledVocabSerializer):
    """The serializer for List Types."""

    class Meta(ControlledVocabSerializer.Meta):
        model = ListType


class IdentifierTypeSerializer(ControlledVocabSerializer):
    """The serializer for List Types."""

    class Meta(ControlledVocabSerializer.Meta):
        model = IdentifierType
